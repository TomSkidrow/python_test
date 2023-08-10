import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
import pandas as pd
import logging
import time

enable_default_logging()

# ค่าเริ่มต้น
VTN_URL = 'http://localhost:9000/OpenADR2/Simple/2.0b'
time.sleep(10)

# นำเข้าข้อมูล
url = 'http://peaoc.pea.co.th/loadprofile/files/04/dt04220111.xls'
df = pd.read_excel(url, sheet_name='Source', skiprows=4, names=['TIME', 'PEAKDAY', 'WORKDAY', 'SATURDAY', 'SUNDAY', 'HOLIDAY'])
valid_df = df.copy()
valid_df.iloc[0:95,1:] = df.iloc[1:96,1:]
valid_df.drop(96, inplace=True)
valid_df.TIME = pd.to_datetime(valid_df.TIME)
valid_df.set_index('TIME', inplace=True)
hr_df = valid_df.resample('H').mean()
hr = 0

# ถูกเรียกเมื่อครบกำหนดเวลา
async def collect_report_value():
    global hr
    value = hr_df.WORKDAY[hr]/1000
    hr += 1
    if hr == 24:
        hr = 0
    return value

# ถูกเรียกเมื่อมีการส่ง event มา
async def handle_event(event):
    logging.info('Got event:', event)
    return 'optIn'

# สร้าง VEN
client = OpenADRClient(ven_name='ven_PEA',
                       vtn_url=VTN_URL)

# ลงทะเบียนกับ VTN
client.add_report(callback=collect_report_value,
                  resource_id='device001',
                  measurement='voltage',
                  sampling_rate=timedelta(seconds=2))

# ลงทะเบียน callback สำหรับ event
client.add_handler('on_event', handle_event)

# สั่งให้ VEN ทำงาน
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()