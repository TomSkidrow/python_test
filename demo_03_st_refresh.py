import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

st_autorefresh(interval=1000, key='refresher')

st.title('ข้อมูลการใช้ไฟฟ้าของ PEA')

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.1':7, 'กฟก.2':8, 'กฟก.3':9}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย':10, 'บ้านอยู่อาศัย > 150 หน่วย':11}
months = {'มกราคม':1, 'กุมภาพันธ์':2, 'มีนาคม':3, 'เมษายน':4, 'พฤษภาคม':5, 'มิถุนายน':6, 'กรกฎาคม':7, 'สิงหาคม':8, 'กันยายน':9, 'ตุลาคม':10, 'พฤศจิกายน':11, 'ธันวาคม':12}
years = {'2565':22, '2564':21, '2563':20}

if 'hour' not in st.session_state:
    st.session_state['hour'] = 0
if 'running' not in st.session_state:
    st.session_state['running'] = False

# นำเข้าข้อมูล
@st.cache_data
def import_data(area_id, cust_id, month, year):
    print('import_data')
    area_id = area_ids[area_id]
    cust_id = cust_ids[cust_id]
    month = months[month]
    year = years[year]
    url = base_url%(area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=['TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95,1:] = df.iloc[1:96,1:]
    valid_df.drop(96, inplace=True)
    valid_df.TIME = pd.to_datetime(valid_df.TIME)
    hr_df = valid_df.set_index('TIME').resample('H').mean()
    return hr_df

# เริ่มการ refresh
def start_update():
    st.session_state['running'] = True

# หยุดการ refresh
def stop_update():
    st.session_state['running'] = False

# UI ส่วนแสดงผล
if st.session_state['running']:
    st.session_state['hour'] += 1
    if st.session_state['hour'] > 23:
        st.session_state['hour'] = 0

cust_id = st.sidebar.selectbox('Customer type', options=cust_ids.keys())
month = st.sidebar.selectbox('Month', options=months.keys())
year = st.sidebar.selectbox('Year', options=years.keys())

# ปรับรูปแบบปุ่มกด
if not st.session_state['running']:
    st.sidebar.button('Start', on_click=start_update)
else:
    st.sidebar.button('Stop', on_click=stop_update)

# UI ส่วนเงื่อนไข
area_txt = list(area_ids.keys())
area1, area2, area3 = st.tabs(area_txt)

# การแสดงผล tab แรก
with area1:
    df = import_data(area_txt[0], cust_id, month, year)
    st.write('### ค่าการใช้ไฟฟ้าชั่วโมง {} คือ {:.2f} kW'.format(st.session_state['hour'], df.WORKDAY.iloc[st.session_state['hour']]))
    st.line_chart(df)

# การแสดงผล tab สอง
with area2:
    df = import_data(area_txt[1], cust_id, month, year)
    st.write('### ค่าการใช้ไฟฟ้าชั่วโมง {} คือ {:.2f} kW'.format(st.session_state['hour'], df.WORKDAY.iloc[st.session_state['hour']]))
    st.line_chart(df)

# การแสดงผล tab สาม
with area3:
    df = import_data(area_txt[2], cust_id, month, year)
    st.write('### ค่าการใช้ไฟฟ้าชั่วโมง {} คือ {:.2f} kW'.format(st.session_state['hour'], df.WORKDAY.iloc[st.session_state['hour']]))
    st.line_chart(df)
