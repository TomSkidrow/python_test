from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import asyncio
from openleadr import OpenADRServer, enable_default_logging
import aiosqlite
from datetime import datetime, timezone, timedelta
from functools import partial
import logging

enable_default_logging()

DB_FILE = 'adr_dbase.db'

# เตรียมฐานข้อมูล
async def init_db():
    logging.info('Database initialized')
    db = await aiosqlite.connect(DB_FILE)
    await db.execute('''CREATE TABLE IF NOT EXISTS ven_list (
                     _id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                     ven_name TEXT,
                     ven_id TEXT,
                     registration_id TEXT)
                     ''')
    await db.execute('''CREATE TABLE IF NOT EXISTS report_list (
                     _id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                     ven_id TEXT,
                     resource_id TEXT,
                     measurement TEXT,
                     value REAL)
                     ''')
    await db.commit()
    await db.close()

# ลงทะเบียน VEN
async def on_create_party_registration(registration_info):
    if registration_info['ven_name'] == 'ven_PEA':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        # บันทึก VEN ลงฐานข้อมูล
        return ven_id, registration_id
    else:
        return False

# ลงทะเบียน report
async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

# อัพเดท report
async def on_update_report(data, ven_id, resource_id, measurement):
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")
        # บันทึก report ลงฐานข้อมูล
        # พยากรณ์การใช้พลังงานด้วยข้อมูลย้อนหลัง 3 วัน

# เตรียม VTN server
vtn_server = OpenADRServer(vtn_id='PEA_DR', http_port=9000)
vtn_server.add_handler('on_create_party_registration', on_create_party_registration)
vtn_server.add_handler('on_register_report', on_register_report)

# เตรียมบริการ FastAPI และ VTN server
app = FastAPI()
asyncio.create_task(init_db())
asyncio.create_task(vtn_server.run())

# สืบค้นข้อมูลจากตาราง ven_list
@app.get("/ven_list")
async def on_ven_list():
    db = await aiosqlite.connect(DB_FILE)
    cursor = await db.execute(f'SELECT * FROM ven_list')
    rows = await cursor.fetchall()
    await db.close()
    return jsonable_encoder(rows)

# สืบค้นข้อมูลจากตาราง report_list
@app.get("/report_list")
async def on_report_list():
    db = await aiosqlite.connect(DB_FILE)
    cursor = await db.execute(f'SELECT * FROM report_list')
    rows = await cursor.fetchall()
    await db.close()
    return jsonable_encoder(rows)
