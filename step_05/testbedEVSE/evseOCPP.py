import asyncio
import websockets
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
import pandas as pd
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
CPO_df = pd.read_csv('CPO_list.csv', skipinitialspace=True)

class evseOCPP(cp):
    def __init__(self, evse_id: str):
        super().__init__(evse_id, None)
        cpo_url = os.getenv("CPO_URL")
        cpo_id = CPO_df.loc[CPO_df.evse_id==self.id, 'cpo_id'].values[0]
        port = CPO_df.loc[CPO_df.evse_id==self.id, 'port'].values[0]
        self._cpo_url = cpo_url%(cpo_id,port)
        self.logger = logging.getLogger('EVSE_CP')

    async def _charger_loop(self, term_queue: asyncio.Queue):
        async with websockets.connect(
            self._cpo_url + self.id, 
            subprotocols=["ocpp1.6"]
        ) as ws:
            self._connection = ws
            await asyncio.gather(self.start(), self.send_boot_notification())
    
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="VOLTA_50", charge_point_vendor="PEA"
        )
        resp = await self.call(request)
        if resp.status == RegistrationStatus.accepted:
            logging.info("Connected to central system")
    
    async def send_start_transaction(self, ev_id: str):
        request = call.StartTransactionPayload(
            connector_id=1, id_tag=ev_id, meter_start=0, timestamp=datetime.now().isoformat()
        )
        resp = await self.call(request)
        logging.info(resp)