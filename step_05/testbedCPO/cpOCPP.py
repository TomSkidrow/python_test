from fastapi import WebSocket
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# websocket adapter
class WebSocketAdapter:
    def __init__(self, websocket: WebSocket):
        self._ws = websocket
        logging.info(self._ws)

    async def recv(self) -> str:
        return await self._ws.receive_text()

    async def send(self, msg) -> str:
        await self._ws.send_text(msg)

# charge point handler
class cpOCPP(cp):
    def __init__(self, evse_id: str, websocket: WebSocket):
        #super().__init__(evse_id, WebSocketAdapter(websocket))
        super().__init__(evse_id, websocket)
        self.logger = logging.getLogger('CP_OCPP')

    @on(Action.Heartbeat)        # this is an OCPP function, not important here
    async def on_heartbeat(self):
        logging.info("heart beat received from chargepoint")
        return call_result.HeartbeatPayload(current_time=datetime.utcnow().isoformat())

    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted,
        )
    
    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, **kwargs):
        return call_result.StartTransactionPayload(
            transaction_id=1,
            id_tag_info={'status': 'Accepted'},
        )