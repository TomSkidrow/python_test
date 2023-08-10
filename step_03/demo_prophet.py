import pandas as pd
import numpy as np
import prophet
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
    valid_df.TIME = pd.to_datetime(valid_df.TIME)
    valid_df.set_index('TIME', inplace=True)
    hr_df = valid_df.resample('H').mean()
    return hr_df/1000.0

# เตรียมชุดข้อมูล
@st.cache_data
def prepare_dataset(df):
    raw_df = pd.concat([df.WORKDAY, df.SATURDAY, df.SUNDAY], ignore_index=True)
    t = pd.date_range(start=df.index[0], periods=len(raw_df), freq='H')
    raw_df.index = t
    return raw_df

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
import_tab, predict_tab = st.tabs(['ชุดข้อมูล', 'พยากรณ์'])

# tab นำเข้าข้อมูล
with import_tab:
    df = import_data(area_id, cust_id, year, month)
    st.line_chart(df, y=['WORKDAY', 'SATURDAY', 'SUNDAY'])
    ds = prepare_dataset(df)
    st.line_chart(ds)
    st.write(ds)

with predict_tab:
    predict_btn = st.button('พยากรณ์', key='predict_btn')
    if predict_btn:
        mdl = prophet.Prophet()
        mdl.fit(ds.reset_index().rename(columns={'index':'ds', 0:'y'}))
        future = mdl.make_future_dataframe(periods=72, freq='H', include_history=False)
        forecast = mdl.predict(future)
        st.line_chart(forecast, y=['yhat', 'yhat_lower', 'yhat_upper'])
        RMSE, MAPE = comp_perf(ds.values, forecast.yhat.values)
        st.write('RMSE = %.2f, MAPE = %.2f'%(RMSE,MAPE))