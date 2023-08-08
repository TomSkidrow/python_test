import streamlit as st
import pandas as pd

# ค่าเริ่มต้น
df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 30]})
count = 0.

# UI ส่วนหลัก
st.write('# Hello World')
st.dataframe(df)
st.line_chart(df)
plus_1 = st.button('บวก 1')
if plus_1:
    st.session_state.count_slider += 1
new_count = st.slider('ตัวเลข', key='count_slider', min_value=-5.,
                      max_value=5., value=count, step=0.1)
st.write(f'ค่าเดิม: {count}, ค่าใหม่: {new_count}')
