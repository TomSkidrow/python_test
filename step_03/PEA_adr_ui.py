import streamlit as st
import pandas as pd
import json
import urllib.request

st.title('PEA DR')

st.sidebar.image('PEA VOLTA.png', width=200)
update_flag = st.sidebar.button('เช็คสถานะ')

if update_flag:
    resp = urllib.request.urlopen(f'http://localhost:8000/report_list')
    resp = json.load(resp)
    df = pd.DataFrame(resp, columns=['_id', 'timestamp', 'ven_id', 'resource_id', 'measurement', 'value'])
    st.write(df)
