#! /bin/bash
uvicorn PEA_adr_vtn:app --reload --host 0.0.0.0 --port 8000 &
streamlit run PEA_adr_ui.py --server.port 8080 --server.address 0.0.0.0 &
python PEA_adr_ven.py
