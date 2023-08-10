import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
import logging

enable_default_logging()

# ค่าเริ่มต้น
VTN_URL = 'http://localhost:8000/OpenADR2/Simple/2.0b'

# ถูกเรียกเมื่อครบกำหนดเวลา
async def collect_report_value():
    return 220.0

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