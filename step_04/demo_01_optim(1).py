import streamlit as st
import pulp as pl
import logging

logging.basicConfig(level=logging.INFO)

# ค่าเริ่มต้น
var_df = pd.DataFrame([
    {'variable': 'a', 'weight': 0.5, 'value': 1.0},
    {'variable': 'b', 'weight': 0.7, 'value': 2.0},
    {'variable': 'c', 'weight': 0.2, 'value': 3.0},
])

# กำหนดเงื่อนไข


def define_constraints(prob, vars, df, limit):
    prob += pl.lpSum([vars[0]*df.weight[0], vars[1] *
                     df.weight[1], vars[2]*df.weight[2]]) <= limit
    return prob

# กำหนดเป้าหมาย


def define_obj_fn(prob, vars, df):
    prob += pl.lpSum([vars[0]*df.value[0], vars[1] *
                     df.value[1], vars[2]*df.value[2]])
    return prob


# UI ส่วนตั้งค่า
st.sidebar.image('PEA VOLTA.png', width=200)
prob_type = st.sidebar.selectbox('เป้าหมาย', ['minimize', 'maximize'])
limit = st.sidebar.slider('ขีดจำกัด', min_value=0.0,
                          max_value=1.0, value=1.0, step=0.1)
solve_flag = st.sidebar.button('แก้ปัญหา', key='solve_btn')

# UI ส่วนแสดงผล
st.subheader('การแก้ปัญหา Knapsack')
df = st.data_editor(var_df, num_rows="dynamic")

st.subheader('ผลลัพธ์')
if solve_flag:
    # กำหนดตัวแปร
    vars = pl.LpVariable.dicts("var", df.index, 0, 1, pl.LpInteger)
    print(vars)
    # กำหนดปัญหา
    if prob_type == 'minimize':
        prob = pl.LpProblem("Knapsack", pl.LpMinimize)
    else:
        prob = pl.LpProblem("Knapsack", pl.LpMaximize)
    define_obj_fn(prob, vars, df)
    # กำหนดเงื่อนไข
    define_constraints(prob, vars, df, limit)
    # หาคำตอบ
    print(prob)
    prob.solve()
    # แสดงผล
    st.write(pl.LpStatus[prob.status])
    st.write(pl.value(prob.objective))
    var_df['selected'] = [pl.value(vars[i]) for i in df.index]
    st.dataframe(var_df)
