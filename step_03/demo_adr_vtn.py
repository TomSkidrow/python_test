import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial

enable_default_logging()

# ถูกเรียกเมื่อมี VEN ลงทะเบียน
async def on_create_party_registration(registration_info):
    if registration_info['ven_name'] == 'ven_PEA':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        return ven_id, registration_id
    else:
        return False

# ถูกเรียกเมื่อมีการลงทะเบียน report จาก VEN
async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

# ถูกเรียกเมื่อมีการ update report จาก VEN
async def on_update_report(data, ven_id, resource_id, measurement):
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")

# ถูกเรียกเมื่อมีการตอบกลับ event
async def event_response_callback(ven_id, event_id, opt_type):
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")

# สร้าง VTN
server = OpenADRServer(vtn_id='vtn_PEA', http_port=8000)

# ลงทะเบียน callback สำหรับการลงทะเบียน
server.add_handler('on_create_party_registration', on_create_party_registration)
server.add_handler('on_register_report', on_register_report)

# เตรียม event ให้ VEN
server.add_event(ven_id='ven_id_123',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{'dtstart': datetime.now(timezone.utc),
                             'duration': timedelta(seconds=10),
                             'signal_payload': 1}],
                 callback=event_response_callback)

# สั่งให้ VTN ทำงาน
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()