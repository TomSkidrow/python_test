from fastapi import FastAPI, Request
from openleadr import OpenADRServer, enable_default_logging
from functools import partial
from datetime import timedelta
import pandas as pd
import logging
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
enable_default_logging()

# OpenADR handler: party registration
async def on_create_party_registration(registration_info):
    global VEN_list
    ven_name = registration_info['ven_name']
    try:
        print(f"VEN {ven_name} is trying to register")
        ven_id = VEN_list.loc[VEN_list.ven_name==ven_name, 'ven_id'].values[0]
        reg_id = VEN_list.loc[VEN_list.ven_name==ven_name, 'reg_id'].values[0]
        return ven_id, reg_id
    except:
        return False

# OpenADR handler: report registration
async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

# OpenADR handler: report update
async def on_update_report(data, ven_id, resource_id, measurement):
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")

# OpenADR service
vtn_server = OpenADRServer(vtn_id=os.getenv('VTN_ID'), 
                           requested_poll_freq=timedelta(seconds=30),
                           http_port=os.getenv('VTN_PORT'), http_host='0.0.0.0')
vtn_server.add_handler('on_create_party_registration', on_create_party_registration)
vtn_server.add_handler('on_register_report', on_register_report)
VEN_list = pd.read_csv('VEN_list.csv', skipinitialspace=True)

# open services
app = FastAPI()
asyncio.create_task( vtn_server.run() )
