import os
from typing import Optional, List

from pyxui import XUI
import uuid


class XUICli:
    def __init__(self):
        self.client: XUI = (XUI(
            full_address='https://testnamehost.ddns.net:54321',
            panel='sanaei'
        ))
        self.client.login(
            os.environ['XUI_LOGIN'],
            os.environ['XUI_PASS'],
        )
        return

    def get_server(self) -> dict:
        return self.client.get_inbound(1)['obj']

    def get_client(self, client_id: str) -> Optional[dict]:
        res = self.client.get_client(1, client_id)

        if res is None:
            return None

        return res

    def create_client(self, client_id: str) -> str:
        client_uuid = str(uuid.uuid4())

        self.client.add_client(
            1,
            client_id + '_' + client_uuid,
            client_uuid)

        return client_uuid

    def delete_client(self, client_id: str) -> None:
        self.client.delete_client(
            1,
            client_id)
        return

