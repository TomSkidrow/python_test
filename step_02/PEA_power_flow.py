import streamlit as st
import pandapower as pp
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.3': 9, 'กฟต.3': 12, 'กฟฉ.1': 4}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย': 10, 'บ้านอยู่อาศัย > 150 หน่วย': 11}
months = {'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4, 'พฤษภาคม': 5, 'มิถุนายน': 6,
          'กรกฎาคม': 7, 'สิงหาคม': 8, 'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12}
years = {'2565': 22, '2564': 21}

net_file = 'PEA_cpo_feeder.py'
net = None

EVSE_TYPE = {'AC Type 2': 43, 'DC CHAdeMO 50 kW': 50,
             'DC CCS 50 kW': 50, 'DC CCS 120 kW': 120}

CPO_df = pd.DataFrame([
    {'name': 'สถานีแรก', 'charger': list(
        EVSE_TYPE.keys())[0], 'number':4, 'bus':1, 'in_service':False},
    {'name': 'สถานีที่สอง', 'charger': list(
        EVSE_TYPE.keys())[0], 'number':4, 'bus':2, 'in_service':False},
    {'name': 'สถานีที่สาม', 'charger': list(
        EVSE_TYPE.keys())[0], 'number':4, 'bus':3, 'in_service':False},
    {'name': 'สถานีที่สี่', 'charger': list(
        EVSE_TYPE.keys())[0], 'number':4, 'bus':4, 'in_service':False}
])

st.session_state.net = None
st.session_state.df = None
st.session_state.cpo_df = None

# นำเข้าข้อมูล


@st.cache_data
def import_data(area_id, cust_id, year, month):
    logging.info('Importing data')
    url = base_url % (area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=[
                       'TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95, 1:] = df.iloc[1:96, 1:]
    valid_df.drop(96, inplace=True)
    return valid_df


# UI ส่วนควบคุม
st.sidebar.image('PEA VOLTA.png', width=200)
area_id = area_ids[st.sidebar.selectbox('เขตการไฟฟ้า', list(area_ids.keys()))]
cust_id = cust_ids[st.sidebar.selectbox('ประเภทลูกค้า', list(cust_ids.keys()))]
year = years[st.sidebar.selectbox('ปี', list(years.keys()))]
month = months[st.sidebar.selectbox('เดือน', list(months.keys()))]
scale = st.sidebar.slider('Scale', min_value=0.0,
                          max_value=1.0, value=1.0, step=0.01, key='scale')
sim_flag = st.sidebar.button('จำลอง', key='sim_btn')

# UI ส่วนแสดงผล
net_tab, load_tab, cpo_tab, sim_tab = st.tabs(
    ['โครงข่าย', 'โหลดพื้นฐาน', 'สถานีอัดประจุ', 'จำลอง'])

# นำเข้าโครงข่าย
with net_tab:
    exec(open(net_file).read())
    st.write('**บัส**')
    st.write(net.bus)
    st.write('**โหลด**')
    st.write(net.load)
    st.session_state.net = net

# นำเข้าข้อมูล
with load_tab:
    df = import_data(area_id, cust_id, year, month)
    st.write('**ข้อมูลการใช้ไฟฟ้า**')
    st.dataframe(df)
    st.session_state.load_df = df

# ข้อมูลสถานีอัดประจุ
with cpo_tab:
    df = st.data_editor(CPO_df,
                        column_config={
                            'name': {'editable': False},
                            'charger': st.column_config.SelectboxColumn(
                                options=EVSE_TYPE.keys(),
                            ),
                        },
                        width=1000
                        )
    st.session_state.cpo_df = df

# จำลองเครือข่าย
with sim_tab:
    if sim_flag:
        pass
