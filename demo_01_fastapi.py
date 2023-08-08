from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
import asyncio
import aiosqlite
import logging

logging.basicConfig(level=logging.INFO)

# ค่าเริ่มต้น
DB_FILE = 'mock_crud.db'

# เตรียมฐานข้อมูล


async def init_db():
    db = await aiosqlite.connect(DB_FILE)
    await db.execute('''
                     CREATE TABLE IF NOT EXISTS evse (
                     _id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                     evse_id TEXT,
                     op TEXT,
                     param TEXT)
                     ''')
    await db.commit()
    await db.close()
    logging.info('Database initialized.')

# เปิดบริการ REST API
app = FastAPI()
asyncio.run(init_db())

# endpoint ทดสอบการรับ parameter


@app.get("/param")
async def on_param(evse_id: str):
    logging.info(f'on_param(): evse_id={evse_id}')
    return jsonable_encoder({'evse_id': evse_id})

# endpoint ทดสอบการรับ JSON


@app.post("/json/{evse_id}")
async def on_json(evse_id: str, request: Request):
    req = await request.json()
    logging.info(f'on_json(): evse_id={evse_id}, req={req}')
    req['evse_id'] = evse_id
    return jsonable_encoder(req)

# endpoint ทดสอบการทำงาน CRUD {'op': ?, 'param': ?}


@app.post("/crud/{evse_id}")
async def on_crud(evse_id: str, request: Request):
    req = await request.json()
    logging.info(f'on_crud(): evse_id={evse_id}, req={req}')
    resp = {}
    if req['op'] == 'create':
        db = await aiosqlite.connect(DB_FILE)
        await db.execute('''INSERT INTO evse (evse_id, op, param) VALUES (?, ?, ?)''',
                         (evse_id, req['op'], req['param']))
        await db.commit()
        await db.close()
        resp['status'] = 'ok'
    elif req['op'] == 'read':
        # query for record with similar param
        db = await aiosqlite.connect(DB_FILE)
        cursor = await db.execute('''SELECT * FROM evse WHERE param = ?''', (req['param'],))
        resp['data'] = await cursor.fetchall()
        await db.close()
    elif req['op'] == 'update':
        pass  # update record with similar evse_id
    elif req['op'] == 'delete':
        pass  # delete record with similar evse_id and param
    else:
        resp['status'] = 'unknown op'
    return jsonable_encoder(resp)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
