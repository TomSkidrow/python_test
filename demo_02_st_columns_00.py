import streamlit as st
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

# ... (existing code for data and UI setup)

# UI ส่วนพื้นฐาน
st.title('ข้อมูลการใช้ไฟฟ้าของ PEA')
st.write('## เลือกข้อมูลเพื่อเปรียบเทียบ')

# Initialize variables to hold calculated load factor values using st.session_state
if 'load_factor_ref' not in st.session_state:
    st.session_state.load_factor_ref = None
if 'load_factor_comp' not in st.session_state:
    st.session_state.load_factor_comp = None

# Create placeholders to display calculated load factor values
load_factor_ref_placeholder = st.empty()
load_factor_comp_placeholder = st.empty()

# UI ส่วนเลือกข้อมูล
col1, col2 = st.columns(2)

with col1:
    if st.checkbox('ข้อมูลอ้างอิง'):
        area_id = st.selectbox('Area', options=area_ids.keys(), key='area1_id')
        cust_id = st.selectbox(
            'Customer type', options=cust_ids.keys(), key='cust1_id')
        month = st.selectbox('Month', options=months.keys(), key='month1')
        year = st.selectbox('Year', options=years.keys(), key='year1')

        if st.button('นำเข้า', key='update_btn1'):
            df = import_data(area_id, cust_id, month, year)
            load_factor_ref_value = df.WORKDAY.max() / df.WORKDAY.mean()
            st.session_state.load_factor_ref = load_factor_ref_value
            load_factor_ref_placeholder.write(
                '### ค่า load factor ในวันทำงาน (อ้างอิง)')
            load_factor_ref_placeholder.write(
                '# {:.4f}'.format(load_factor_ref_value))

# Display load factor value for reference data
if st.session_state.load_factor_ref is not None:
    load_factor_ref_placeholder.write(
        '### ค่า load factor ในวันทำงาน (อ้างอิง)')
    load_factor_ref_placeholder.write(
        '# {:.4f}'.format(st.session_state.load_factor_ref))

with col2:
    if st.checkbox('ข้อมูลเปรียบเทียบ'):
        area_id = st.selectbox('Area', options=area_ids.keys(), key='area2_id')
        cust_id = st.selectbox(
            'Customer type', options=cust_ids.keys(), key='cust2_id')
        month = st.selectbox('Month', options=months.keys(), key='month2')
        year = st.selectbox('Year', options=years.keys(), key='year2')

        if st.button('นำเข้า', key='update_btn2'):
            df = import_data(area_id, cust_id, month, year)
            load_factor_comp_value = df.WORKDAY.max() / df.WORKDAY.mean()
            st.session_state.load_factor_comp = load_factor_comp_value
            load_factor_comp_placeholder.write(
                '### ค่า load factor ในวันทำงาน (เปรียบเทียบ)')
            load_factor_comp_placeholder.write(
                '# {:.4f}'.format(load_factor_comp_value))

# Display load factor value for comparison data
if st.session_state.load_factor_comp is not None:
    load_factor_comp_placeholder.write(
        '### ค่า load factor ในวันทำงาน (เปรียบเทียบ)')
    load_factor_comp_placeholder.write(
        '# {:.4f}'.format(st.session_state.load_factor_comp))
