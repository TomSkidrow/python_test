import streamlit as st
import pandapower as pp

# ค่าเริ่มต้น
NET_FILES = {'โครงข่าย #1':'demo_network_01.py', 'โครงข่าย #2':'demo_network_02.py'}
net = None

# UI ส่วนควบคุม
st.sidebar.image('PEA VOLTA.png', width=200)
st.sidebar.selectbox('ไฟล์ของโครงข่าย', options=NET_FILES.keys(), key='network_file')
st.sidebar.button('จำลอง', key='sim_network')

# UI ส่วนแสดงผล
st.subheader('การจำลองระบบไฟฟ้าด้วย pandapower')
net_tab, res_tab = st.tabs(['ข้อมูลโครงข่าย', 'ผลการจำลอง'])

net_file = NET_FILES[st.session_state.network_file]
exec( open(net_file).read() )

# UI แสดงข้อมูลโครงข่าย
with net_tab:
    if net:
        st.write('**บัส**')
        st.write(net.bus)
        st.write('**โหลด**')
        st.write(net.load)
        st.write('**สายส่ง**')
        st.write(net.line)
        st.write('**หม้อแปลง**')
        st.write(net.trafo)

# UI แสดงผลการจำลอง
if st.session_state.sim_network:
    if net:
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