import streamlit as st
import streamlit_autorefresh as st_autorefresh
import pandas as pd
import urllib.request
from dotenv import load_dotenv
load_dotenv()

# CPO setting
CPO_df = pd.DataFrame([
    {'name': 'PEA_A', 'chargingP': 50., 'number': 4, 'in_service': True},
    {'name': 'PEA_B', 'chargingP': 50., 'number': 4, 'in_service': True},
    {'name': 'PEA_C', 'chargingP': 50., 'number': 4, 'in_service': True},
    {'name': 'PEA_D', 'chargingP': 50., 'number': 4, 'in_service': True},
    {'name': 'PEA_E', 'chargingP': 50., 'number': 4, 'in_service': True}
])

st.sidebar.image("PEA VOLTA.png", width=200)
start_btn = st.sidebar.button("Start")

evTab, evseTab, cpoTab, dsoTab = st.tabs(["EV", "EVSE", "CPO", "DSO"])

# UI ส่วน EVSE
with evseTab:
    df = st.data_editor(CPO_df)

# UI ส่วน EV
with evTab:
    pass

# UI ส่วน CPO
with cpoTab:
    pass

# UI ส่วน DSO
with dsoTab:
    pass

# start operation
if start_btn:
    pass