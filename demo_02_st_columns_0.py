import streamlit as st
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.1':7, 'กฟก.2':8, 'กฟก.3':9}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย':10, 'บ้านอยู่อาศัย > 150 หน่วย':11}
months = {'มกราคม':1, 'กุมภาพันธ์':2, 'มีนาคม':3, 'เมษายน':4, 'พฤษภาคม':5, 'มิถุนายน':6, 'กรกฎาคม':7, 'สิงหาคม':8, 'กันยายน':9, 'ตุลาคม':10, 'พฤศจิกายน':11, 'ธันวาคม':12}
years = {'2565':22, '2564':21, '2563':20}

# นำเข้าข้อมูล
@st.cache_data
def import_data(area_id, cust_id, month, year):
    logging.info(f'import_data(): area_id={area_id}, cust_id={cust_id}, month={month}, year={year}')
    area_id = area_ids[area_id]
    cust_id = cust_ids[cust_id]
    month = months[month]
    year = years[year]
    url = base_url%(area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=['TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95,1:] = df.iloc[1:96,1:]
    valid_df.drop(96, inplace=True)
    return valid_df

# UI ส่วนพื้นฐาน
st.title('ข้อมูลการใช้ไฟฟ้าของ PEA')
st.write('## เลือกข้อมูลเพื่อเปรียบเทียบ')

# UI ส่วนเลือกข้อมูล
col1, col2 = st.columns(2)
with col1:
    if st.checkbox('ข้อมูลอ้างอิง'):
        area_id = st.selectbox('Area', options=area_ids.keys(), key='area1_id')
        cust_id = st.selectbox('Customer type', options=cust_ids.keys(), key='cust1_id')
        month = st.selectbox('Month', options=months.keys(), key='month1')
        year = st.selectbox('Year', options=years.keys(), key='year1')
        df = import_data(area_id, cust_id, month, year)
        st.write('### ค่า load factor ในวันทำงาน')
        st.write('# {:.4f}'.format(df.WORKDAY.max()/df.WORKDAY.mean()))

with col2:
    if st.checkbox('ข้อมูลเปรียบเทียบ'):
        area_id = st.selectbox('Area', options=area_ids.keys(), key='area2_id')
        cust_id = st.selectbox('Customer type', options=cust_ids.keys(), key='cust2_id')
        month = st.selectbox('Month', options=months.keys(), key='month2')
        year = st.selectbox('Year', options=years.keys(), key='year2')
        df = import_data(area_id, cust_id, month, year)
        st.write('### ค่า load factor ในวันทำงาน')
        st.write('# {:.4f}'.format(df.WORKDAY.max()/df.WORKDAY.mean()))