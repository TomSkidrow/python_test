import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import keras
from keras import layers
from tensorflow import keras
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)

base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.3':9, 'กฟต.3':12, 'กฟฉ.1':4}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย':10, 'บ้านอยู่อาศัย > 150 หน่วย':11}
months = {'มกราคม':1, 'กุมภาพันธ์':2, 'มีนาคม':3, 'เมษายน':4, 'พฤษภาคม':5, 'มิถุนายน':6, 'กรกฎาคม':7, 'สิงหาคม':8, 'กันยายน':9, 'ตุลาคม':10, 'พฤศจิกายน':11, 'ธันวาคม':12}
years = {'2565':22, '2564':21}

# นำเข้าข้อมูล
@st.cache_data
def import_data(area_id, cust_id, year, month):
    logging.info('Importing data')
    url = base_url%(area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=['TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95,1:] = df.iloc[1:96,1:]
    valid_df.drop(96, inplace=True)
    return valid_df

# เตรียมชุดข้อมูล
@st.cache_data
def prepare_dataset(df, seq_len, seq_ahead):
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_train_df = scaler.fit_transform(df.values.reshape(-1, 1))
    seqs = scaled_train_df.shape[0] - seq_len - seq_ahead
    features = []
    labels_dict = {i:[] for i in range(seq_ahead)}
    scaled_train_df = scaled_train_df.reshape(-1, 1)
    for i in range(seqs):
        features.append( scaled_train_df[i:seq_len+i, 0] ) 
        for j in range(seq_ahead):
            labels_dict[j].append( scaled_train_df[seq_len+i+j, 0] ) 
    features = np.array(features)
    features = np.reshape(features, (features.shape[0], features.shape[1], 1))
    labels_list = []
    for i in range(seq_ahead):
        labels_list.append( np.array(labels_dict[i]).reshape(-1,1) )
    feat_tensor = np.concatenate([features]*seq_ahead, axis=2)
    label_tensor = np.concatenate(labels_list, axis=1)
    return (feat_tensor, label_tensor, scaler)

# เตรียมโมเดล
@st.cache_data
def create_lstm_model(lstm_units, more_layers, seq_len, seq_ahead):
    model = keras.Sequential()
    model.add( layers.LSTM(units=lstm_units, return_sequences=True, activation='tanh', input_shape=(seq_len, seq_ahead)) ) # สร้าง LSTM layer โดยกำหนดขนาดของ feature เป็น จำนวนวันในอดีต x จำนวนวันที่จะพยากรณ์
    model.add( layers.Dropout(0.1) )
    for i in range(more_layers):
        model.add( layers.LSTM(units=lstm_units, return_sequences=True,  activation='tanh') )
        model.add( layers.Dropout(0.1) )
    model.add( layers.LSTM(units=lstm_units, return_sequences=False,  activation='tanh') )
    model.add( layers.Dense(units=seq_ahead, activation='linear') ) 
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# คำนวณตัวชี้วัด
def comp_perf(y, yhat):
    RMSE = np.sqrt( np.sum( (y-yhat)**2 )/len(y) )
    MAPE = 1/len(y) * np.sum(np.abs(y-yhat)/y)*100
    return (RMSE,MAPE)

# สร้าง UI เลือกข้อมูล
st.sidebar.image('PEA VOLTA.png', width=200)
area_id = area_ids[ st.sidebar.selectbox('เขตการไฟฟ้า', list(area_ids.keys())) ]
cust_id = cust_ids[ st.sidebar.selectbox('ประเภทลูกค้า', list(cust_ids.keys())) ]
year = years[ st.sidebar.selectbox('ปี', list(years.keys())) ]
month = months[ st.sidebar.selectbox('เดือน', list(months.keys())) ]

# แสดงเทรนด์ของข้อมูล
st.subheader('แนวโน้มการใช้พลังงานไฟฟ้า')
import_tab, prepare_tab, train_tab, predict_tab = st.tabs(['ข้อมูลดิบ', 'ชุดข้อมูล', 'แบบจำลอง', 'พยากรณ์'])

# tab นำเข้าข้อมูล
with import_tab:
    df = import_data(area_id, cust_id, year, month)
    st.line_chart(df, y=['WORKDAY', 'SATURDAY', 'SUNDAY'])

# tab เตรียมชุดข้อมูล
with prepare_tab:
    seq_len = st.number_input('ความยาว feature', min_value=1, max_value=24, value=12)
    seq_ahead = st.number_input('พยากรณ์ล่วงหน้า', min_value=1, max_value=24, value=12)
    prepare_btn =st.button('เตรียม', key='prepare_btn')
    if prepare_btn:
        raw_df = pd.concat( [df.WORKDAY, df.SATURDAY, df.SUNDAY], ignore_index=True)
        st.line_chart(raw_df)
        feat_tensor, label_tensor, scaler = prepare_dataset(raw_df, seq_len, seq_ahead)
        st.session_state.feat_tensor = feat_tensor
        st.session_state.label_tensor = label_tensor
        st.session_state.scaler = scaler
        logging.info('ชุดข้อมูล', feat_tensor.shape, label_tensor.shape)

with train_tab:
    num_nodes = st.number_input('จำนวนโหนด', min_value=1, max_value=24, value=12)
    num_layers = st.number_input('จำนวนชั้น', min_value=0, max_value=5, value=1)
    num_epochs = st.number_input('รอบการเทรน', min_value=20, max_value=100, value=20)
    train_btn =st.button('เทรน', key='train_btn')
    if train_btn:
        st.session_state.model = create_lstm_model(num_nodes, num_layers, seq_len, seq_ahead)
        st.session_state.model.summary()
        status = st.session_state.model.fit(st.session_state.feat_tensor, st.session_state.label_tensor, epochs=num_epochs, batch_size=32)
        st.line_chart(status.history['loss'])

with predict_tab:
    predict_btn = st.button('พยากรณ์', key='predict_btn')
    if predict_btn:
        predicts = st.session_state.model.predict(st.session_state.feat_tensor)
        RMSE,MAPE = comp_perf(st.session_state.label_tensor[-1,:], predicts[-1,:])
        orig_val = st.session_state.scaler.inverse_transform(st.session_state.label_tensor[-1,:].reshape(-1,1))
        pred_val = st.session_state.scaler.inverse_transform(predicts[-1,:].reshape(-1,1))
        results = np.concatenate( [orig_val,pred_val], axis=1)
        st.write(results)
        st.line_chart(results)
        st.write(f'**RMSE:** {RMSE}, **MAPE:** {MAPE}')