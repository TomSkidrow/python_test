import streamlit as st
import pandas as pd
import pandapower as pp
import pulp as pl
import logging

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.3':9, 'กฟต.3':12, 'กฟฉ.1':4}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย':10, 'บ้านอยู่อาศัย > 150 หน่วย':11}
months = {'มกราคม':1, 'กุมภาพันธ์':2, 'มีนาคม':3, 'เมษายน':4, 'พฤษภาคม':5, 'มิถุนายน':6, 'กรกฎาคม':7, 'สิงหาคม':8, 'กันยายน':9, 'ตุลาคม':10, 'พฤศจิกายน':11, 'ธันวาคม':12}
years = {'2565':22, '2564':21}
demand_df = None

net_file = 'PEA_cpo_feeder.py'
net = None

EVSE_TYPE = {'AC Type 2': 43, 'DC CHAdeMO 50 kW':50, 'DC CCS 50 kW':50, 'DC CCS 120 kW':120}

CPO_df = pd.DataFrame(
    [
        {'name':'สถานีแรก', 'type':list(EVSE_TYPE.keys())[0], 'num_chargers':4, 'bus':1, 'in_service':True},
        {'name':'สถานีที่สอง', 'type':list(EVSE_TYPE.keys())[0], 'num_chargers':4, 'bus':2, 'in_service':True},
        {'name':'สถานีที่สาม', 'type':list(EVSE_TYPE.keys())[0], 'num_chargers':4, 'bus':3, 'in_service':True},
        {'name':'สถานีที่สี่', 'type':list(EVSE_TYPE.keys())[0], 'num_chargers':4, 'bus':4, 'in_service':True},
    ])

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
    return hr_df

# คำนวณภาระโหลดของสถานีอัดประจุไฟฟ้าในหน่วย MW 
def calc_load(CPO_df, cpo_id):
    return 0.0

# คำนวณผลกระทบ %loading สายส่ง ต่อโครงข่ายไฟฟ้า โดยสมมุติว่ามีแค่สถานีเดียว
def calc_impact(net, CPO_df, cpo_id):
    for i in range(len(CPO_df)):
        net.load.p_mw[i] = 0.0
    if cpo_id >= 0:
        cpo_load = calc_load(CPO_df, cpo_id)
        net.load.p_mw[cpo_id] = cpo_load/1000.0
    pp.runpp(net)
    return net.res_line.loading_percent[0]/100.0

# กำหนดเงื่อนไข
def define_constraints(prob, vars, weights, limit):
    num_terms = len(weights)
    prob += pl.lpSum([vars[i]*weights[i] for i in range(num_terms)]) <= limit
    return prob

# กำหนดเป้าหมาย
def define_obj_fn(prob, vars, values):
    num_terms = len(values)
    prob += pl.lpSum([vars[i]*values[i] for i in range(num_terms)])
    return prob

# UI ส่วนตั้งค่า
st.sidebar.image('PEA VOLTA.png', width=200)
area_id = area_ids[ st.sidebar.selectbox('เขตการไฟฟ้า', list(area_ids.keys())) ]
cust_id = cust_ids[ st.sidebar.selectbox('ประเภทลูกค้า', list(cust_ids.keys())) ]
year = years[ st.sidebar.selectbox('ปี', list(years.keys())) ]
month = months[ st.sidebar.selectbox('เดือน', list(months.keys())) ]
scale = st.sidebar.slider('สเกล', min_value=0.0, max_value=1.0, value=0.1, step=0.01)
solve_flag = st.sidebar.button('แก้ปัญหา', key='solve_btn')

# UI ส่วนแสดงผล
st.subheader('load shedding ในมุมมองปัญหา Knapsack')
preview_tab, setting_tab, optimize_tab  = st.tabs(['การใช้ไฟฟ้าพื้นฐาน', 'สถานีชาร์จ EV', 'Optimize'])

# UI ส่วนแสดงข้อมูลพื้นฐาน
with preview_tab:
    demand_df = import_data(area_id, cust_id, year, month)
    st.line_chart(demand_df.WORKDAY)

# UI ตั้งค่าสถานีชาร์จ EV
with setting_tab:
    CPO_df = st.data_editor(CPO_df,
                            column_config={
                       'สถานี': {'editable': False},
                       'ประเภท charger': st.column_config.SelectboxColumn(
                           options=EVSE_TYPE.keys(),
                        ),
                   },
                   width=1000,
                   key='CPO_df'
                   )

# UI ส่วนหาคำตอบ
with optimize_tab:
    if solve_flag:
        for hr in range(0,24):
            weights = []
            values = []
            # เชื่อมต่อโหลด PEAOC ที่บัส 4 และประเมิน %loading ของสายส่ง
            net.load.p_mw[4] = demand_df.WORKDAY[hr]/1000.0 * scale
            base_loading = calc_impact(net, CPO_df, -1)
            net.load.p_mw[4] = 0.0
            for i in range(4):
                # ประเมิน %loading ของสายส่ง เป็น weights และภาระโหลดเป็น values
                weights.append( calc_impact(net, CPO_df, i) )
                values.append( calc_load(CPO_df, i) )
            # หาคำตอบของปัญหา Knapsack โดยใช้ 80% ของสายส่งเป็นขีดจำกัด
            limit = 0.8 - base_loading
            vars = pl.LpVariable.dicts("var", CPO_df.index, 0, 1, pl.LpInteger)
            prob = pl.LpProblem("Knapsack", pl.LpMaximize)
            define_obj_fn(prob, vars, values)
            define_constraints(prob, vars, weights, limit)
            prob.solve()
            st.write(pl.LpStatus[prob.status])
            st.write(pl.value(prob.objective))
        # แสดงกราฟของ %loading ของสายส่งเมื่อ CPO ถูก load shedding
