import pandapower as pp
import pandas as pd
import pandapower.networks as pp_nw
import pandapower.timeseries as pp_ts
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.1': 7, 'กฟก.2': 8, 'กฟก.3': 9}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย': 10, 'บ้านอยู่อาศัย > 150 หน่วย': 11}
months = {'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4, 'พฤษภาคม': 5, 'มิถุนายน': 6,
          'กรกฎาคม': 7, 'สิงหาคม': 8, 'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12}
years = {'2565': 22, '2564': 21, '2563': 20}

# นำเข้าข้อมูล


@st.cache_data
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
    valid_df.TIME = pd.to_datetime(valid_df.TIME)
    # hr_df = valid_df.resample("H").mean()

    return valid_df
    # return hr_df


# UI ส่วนควบคุม
st.sidebar.image('PEA VOLTA.png', width=200)
area_id = st.sidebar.selectbox('Area', options=area_ids.keys(), key='area_id')
cust_id = st.sidebar.selectbox(
    'Customer type', options=cust_ids.keys(), key='cust_id')
month = st.sidebar.selectbox('Month', options=months.keys(), key='month')
year = st.sidebar.selectbox('Year', options=years.keys(), key='year')
scale = st.sidebar.slider('Scale', min_value=0.0,
                          max_value=1.0, value=1.0, step=0.01, key='scale')
sim_flag = st.sidebar.button('จำลอง', key='sim_btn')

# UI ส่วนแสดงผล
net_tab, sim_tab, trend_tab = st.tabs(
    ['ข้อมูลโครงข่าย', 'ผลการจำลอง', 'ผลกระทบต่อสายส่ง'])

# แสดงข้อมูลโครงข่าย
with net_tab:
    net = pp_nw.example_simple()
    st.write('**บัส**')
    st.write(net.bus)
    st.write('**โหลด**')
    st.write(net.load)
    st.write('**สายส่ง**')
    st.write(net.line)
    st.write('**หม้อแปลง**')
    st.write(net.trafo)

# แสดงผลการจำลอง
with sim_tab:
    if sim_flag:
        df = import_data()
        net.load.p_mw[0] = df.WORKDAY[0]/1000.0 * scale
        pp.runpp(net)
        st.write('**บัส**')
        st.write(net.res_bus)
        st.write('**โหลด**')
        st.write(net.res_load)
        st.write('**สายส่ง**')
        st.write(net.res_line)
        st.write('**หม้อแปลง**')
        st.write(net.res_trafo)
    else:
        st.write('**โปรดกดปุ่มจำลอง**')

# แสดงผลกระทบต่อสายส่ง
with trend_tab:
    if sim_flag:
        net.load.p_mw[0] = df.WORKDAY[0]/1000.0 * scale
        pp.runpp(net)
        st.write(f'**สายส่ง** {net.res_line.loading_percent[3]}')
