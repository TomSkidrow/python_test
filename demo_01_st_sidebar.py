import streamlit as st
import pandas as pd

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟฉ.2': 5, 'กฟก.1': 7, 'กฟก.2': 8, 'กฟก.3': 9}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย': 10, 'บ้านอยู่อาศัย > 150 หน่วย': 11}
months = {'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4, 'พฤษภาคม': 5, 'มิถุนายน': 6,
          'กรกฎาคม': 7, 'สิงหาคม': 8, 'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12}
years = {'2565': 22, '2564': 21, '2563': 20}

# นำเข้าข้อมูล


def import_data():
    area_id = area_ids[st.session_state.area_id]
    cust_id = cust_ids[st.session_state.cust_id]
    month = months[st.session_state.month]
    year = years[st.session_state.year]
    url = base_url % (area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=[
                       'TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95, 1:] = df.iloc[1:96, 1:]
    valid_df.drop(96, inplace=True)
    return valid_df


st.title('ข้อมูลการใช้ไฟฟ้าของ PEA')
area_id = st.sidebar.selectbox('Area', options=area_ids.keys(), key='area_id')
cust_id = st.sidebar.selectbox(
    'Customer type', options=cust_ids.keys(), key='cust_id')
month = st.sidebar.selectbox('Month', options=months.keys(), key='month')
year = st.sidebar.selectbox('Year', options=years.keys(), key='year')
update_flag = st.sidebar.button('นำเข้า', key='update_btn')

if update_flag:
    df = import_data()
    st.write(df)
    st.line_chart(df.WORKDAY)
