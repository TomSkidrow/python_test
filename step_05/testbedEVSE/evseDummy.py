from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
import asyncio
import aiosqlite
import logging
from evseOCPP import *
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

DB_FILE = 'testbedEVSE.db'
evse_objs = {}

# initialize internal database
async def init_db():
    db = await aiosqlite.connect(DB_FILE)
    await db.execute('''CREATE TABLE IF NOT EXISTS evse_log (
                     _id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    evse_id TEXT,
                    evse_status TEXT
                    )''')
    await db.execute('''CREATE TABLE IF NOT EXISTS ev_log (
                     _id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                     evse_id TEXT,
                     ev_id TEXT,
                     ev_soc REAL,
                     ev_power REAL,
                     ev_status TEXT
                     )''')
    await db.commit()
    await db.close()

# record evse log
async def record_evse_log(evse_id: str, evse_status: str):
    db = await aiosqlite.connect(DB_FILE)
    await db.execute(f"INSERT INTO evse_log (evse_id, evse_status) VALUES ('{evse_id}', '{evse_status}')")
    await db.commit()
    await db.close()

# record ev log
async def record_ev_log(evse_id: str, ev_id: str, ev_soc: float, ev_power: float, ev_status: str):
    db = await aiosqlite.connect(DB_FILE)
    await db.execute(f"INSERT INTO ev_log (evse_id, ev_id, ev_soc, ev_power, ev_status) VALUES ('{evse_id}', '{ev_id}', {ev_soc}, {ev_power}, '{ev_status}')")
    await db.commit()
    await db.close()

# start instance
app = FastAPI()
asyncio.create_task( init_db() )

# API for query evse_log
@app.get('/evse_log/{evse_id}')
async def on_query_evse_log(evse_id: str):
    db = await aiosqlite.connect(DB_FILE)
    cursor = await db.execute(f"SELECT * FROM evse_log WHERE evse_id='{evse_id}'")
    rows = await cursor.fetchall()
    await db.close()
    return jsonable_encoder(rows)

# API for query ev_log
@app.get('/ev_log/{ev_id}')
async def on_query_ev_log(ev_id: str):
    db = await aiosqlite.connect(DB_FILE)
    cursor = await db.execute(f"SELECT * FROM ev_log WHERE ev_id='{ev_id}'")
    rows = await cursor.fetchall()
    await db.close()
    return jsonable_encoder(rows)

# REST API for SECC operation
@app.post('/secc/{evse_id}')
async def on_secc_api(evse_id: str, request: Request):
    req = await request.json()
    if req['Message'] == 'SessionSetupReq':
        evse_objs[evse_id] = evseOCPP(evse_id)
        term_queue = asyncio.Queue(maxsize=1)
        try:
            evse_task = asyncio.create_task(evse_objs[evse_id]._charger_loop(term_queue))
        except Exception as error:
            logging.warn(f"Charger {cp.id} disconnected: {error}")
        finally:
            del evse_task
            await term_queue.put(True)
        await record_evse_log(evse_id, 'Start')
        resp = {'Message':'SessionSetupRes', 'ResponseCode': 'OK'}
    elif req['Message'] == 'PowerDeliveryReq':
        await evse_objs[evse_id].send_start_transaction(req['EV_ID'])
        await record_ev_log(evse_id, req['EV_ID'], req['EV_SOC'], req['EV_Power'], 'Start')
        resp = {'Message': 'PowerDeliveryRes', 'ResponseCode': 'OK'}
    else:
        resp = {'Message':'Unknown', 'ResponseCode': 'Error'}
    return jsonable_encoder(resp)