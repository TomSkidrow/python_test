from fastapi import FastAPI, Request
from cpOCPP import *
import asyncio
import websockets
from openleadr import OpenADRClient, enable_default_logging
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
enable_default_logging()

# OCPP service via websockets
async def on_connect(websocket, path):
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports  %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()
    evse_id = path.split("/")[-1]
    cp = cpOCPP(evse_id, websocket)
    await cp.start()

# run OCPP service
async def run_ocpp_service():
    ocpp_port = int(os.getenv("CPO_PORT"))
    ocpp_server = await websockets.serve(on_connect, 
                                         "0.0.0.0",
                                         ocpp_port, 
                                         subprotocols=["ocpp1.6"]
                                         )
    await ocpp_server.wait_closed()


# start instance
app = FastAPI()
adr_client = OpenADRClient(ven_name=os.getenv('VEN_NAME'),vtn_url=os.getenv('VTN_URL'))
asyncio.create_task( run_ocpp_service() )
asyncio.create_task( adr_client.run() )
