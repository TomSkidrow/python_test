import streamlit as st
import pandas as pd
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import numpy as np
import logging

# ค่าเริ่มต้น
base_url = 'http://peaoc.pea.co.th/loadprofile/files/%.2d/dt%.2d%.2d%.2d%.2d.xls'
area_ids = {'กฟก.1':7, 'กฟก.2':8, 'กฟก.3':9}
cust_ids = {'บ้านอยู่อาศัย < 150 หน่วย':10, 'บ้านอยู่อาศัย > 150 หน่วย':11}
months = {'มกราคม':1, 'กุมภาพันธ์':2, 'มีนาคม':3, 'เมษายน':4, 'พฤษภาคม':5, 'มิถุนายน':6, 'กรกฎาคม':7, 'สิงหาคม':8, 'กันยายน':9, 'ตุลาคม':10, 'พฤศจิกายน':11, 'ธันวาคม':12}
years = {'2565':22, '2564':21, '2563':20}

PK_PRICE_EFFECT = 0.9
OFPK_PRICE_EFFECT = 1.1

# นำเข้าข้อมูล
def import_data():
    area_id = area_ids[st.session_state.area_id]
    cust_id = cust_ids[st.session_state.cust_id]
    month = months[st.session_state.month]
    year = years[st.session_state.year]
    url = base_url%(area_id, area_id, year, month, cust_id)
    df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=['TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
    valid_df = df.copy()
    valid_df.iloc[0:95,1:] = df.iloc[1:96,1:]
    valid_df.drop(96, inplace=True)
    valid_df.TIME = pd.to_datetime(valid_df.TIME)
    valid_df.set_index('TIME', inplace=True)
    hr_df = valid_df.resample('H').mean()
    return hr_df

# การคำนวณค่าไฟฟ้า (พันล้านบาท)
def calc_income(demand_df, peak_start, peak_end, peak_cost, offpeak_cost):
    income = 0
    for i in range(0, 24):
        if i >= peak_start and i <= peak_end:
            demand = demand_df[i] * PK_PRICE_EFFECT
            income += demand/1000 * peak_cost
        else:
            demand = demand_df[i] * OFPK_PRICE_EFFECT
            income += demand/1000 * offpeak_cost
    return income/1000

# ปรับความต้องการไฟฟ้า
def augment_demand(demand_df, peak_start, peak_end):
    aug_demand = [demand_df[hr]*PK_PRICE_EFFECT/1000 if (hr >= peak_start and hr <= peak_end) else demand_df[hr]*OFPK_PRICE_EFFECT/1000 for hr in range(0,24)]
    return aug_demand

# คลาสสำหรับแก้ปัญหา
class PeakPeriodProblem(ElementwiseProblem):
    def __init__(self, demand_df, max_period):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_ieq_constr=2,
                         xl=np.array([0,0]),
                         xu=np.array([23,23]),
                         vtype=int)
        self.demand_df = demand_df
        self.max_period = max_period

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = np.column_stack([self.cost_fn_income(x), self.cost_fn_peak(x)])
        out["G"] = np.column_stack([self.const_order(x), self.const_period(x)])
    
    # cost function = เพิ่มค่าไฟฟ้า
    def cost_fn_income(self, x):
        income = 0
        return -income/1000

    # cost function = ลดความต้องการไฟฟ้าสูงสุด
    def cost_fn_peak(self, x):
        peak = 0
        return peak
    
    # constraint function = start ก่อน end
    def const_order(self, x):
        return 0

    # constraint function = เวลา peak ไม่เกิน max_period ชั่วโมงต่อวัน
    def const_period(self, x):
        return 0

# UI ส่วนตั้งค่า
st.sidebar.image('PEA VOLTA.png', width=200)
area_id = st.sidebar.selectbox('Area', options=area_ids.keys(), key='area_id')
cust_id = st.sidebar.selectbox('Customer type', options=cust_ids.keys(), key='cust_id')
month = st.sidebar.selectbox('Month', options=months.keys(), key='month')
year = st.sidebar.selectbox('Year', options=years.keys(), key='year')
solve_flag = st.sidebar.button('แก้ปัญหา', key='solve_btn')

# UI ส่วนแสดงผล
st.subheader('การเลือก peak period')
peak_start = 9
peak_end = 22
peak_cost = 4.5
offpeak_cost = 2.5
df = import_data()
st.line_chart(df.WORKDAY)
st.write(f'ค่าไฟช่วง peak {peak_cost} บาท/หน่วย และ off-peak {offpeak_cost} บาท/หน่วย')
income = calc_income(df.WORKDAY, peak_start, peak_end, peak_cost, offpeak_cost)
st.write(f'ค่าไฟฟ้ารวม: {income:.2f} พันล้านบาท และความต้องการไฟฟ้าสูงสุด {max(df.WORKDAY)/1000:.2f} MW')

# เงื่อนไข
st.subheader('เงื่อนไข')
max_period = st.number_input('ช่วง peak ไม่เกินกี่ชั่วโมงต่อวัน', min_value=1, max_value=24, value=8, step=1, key='max_period')
st.subheader('ผลลัพธ์')
if solve_flag:
    problem = PeakPeriodProblem(df.WORKDAY, max_period)
    algorithm = NSGA2(pop_size=100,
                      sampling=IntegerRandomSampling(),
                      crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                      mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                      eliminate_duplicates=True,)
    res = minimize(problem, algorithm, ('n_gen', 50), seed=1, verbose=True)
    print("Best solution found: %s" % res.X)
    print("Function value: %s" % res.F)
    print("Constraint violation: %s" % res.CV)
    sol = res.X[0]
    out = res.F[0]
    st.slider('Peak period', min_value=0, max_value=23, value=[sol[0],sol[1]], step=1, key='peak_period')
    st.write(f'ค่าไฟฟ้ารวม: {-out[0]:.2f} พันล้านบาท และความต้องการไฟฟ้าสูงสุด {out[1]:.2f} MW')
    demands = augment_demand(df.WORKDAY, sol[0], sol[1])
    st.line_chart(demands)
