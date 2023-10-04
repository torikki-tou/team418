from typing import Optional

from pyxui import XUI
from pyxui.errors import BadLogin, NotFound
import uuid

from src.infrastracture.config import config
from src.infrastracture.logger import logger


class XUIClient:
    def __init__(self):
        self.__client: XUI = (XUI(
            full_address=config.get_engine_url(),
            panel='sanaei'
        ))
        if not self.__login():
            logger.critical('xui login unsuccessful')

        self.__default_inbound_id = 1
        return

    def get_server_info(self) -> dict:
        return self.__client.get_inbound(self.__default_inbound_id)['obj']

    def get_client(self, client_id: str) -> Optional[dict]:
        res = self.__client.get_client(self.__default_inbound_id, client_id)

        if res is NotFound:
            return None

        return res

    def create_client(self, prefix: str) -> str:
        client_uuid = str(uuid.uuid4())

        client_id = prefix + '_' + client_uuid if prefix else client_uuid

        self.__client.add_client(
            self.__default_inbound_id,
            client_id,
            client_uuid
        )

        return client_uuid

    def delete_client(self, client_id: str) -> bool:
        try:
            self.__client.delete_client(
                self.__default_inbound_id,
                client_id
            )
        except Exception:
            return False

        return True

    def __login(self) -> bool:
        try:
            self.__client.login(
                username=config.get_engine_username(),
                password=config.get_engine_password(),
            )
        except BadLogin:
            return False

        return True


xui_engine = XUIClient()
