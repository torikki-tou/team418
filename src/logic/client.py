from typing import Optional, List, Dict
import json

from pyxui.config_gen import config_generator

from src.logic.models.client import Client as ClientDTO
from src.data.repo.clientconfig import ClientConfig as ClientRepo
from src.data.engine.xui import XUIClient
from src.infrastracture.config import config


class Client:
    def __init__(self):
        self.client_repo = ClientRepo()
        self.xui = XUIClient()
        return

    def get_by_user(self, user_id: str, offset: int = 0, limit: int = 20) -> List[str]:
        return [cnf.id for cnf in self.client_repo.get_by_user(user_id, offset, limit)]

    def get(self, client_id: str) -> Optional[ClientDTO]:
        db_client = self.client_repo.get(client_id)

        if db_client is None:
            return None

        stream_settings = json.loads(
            self.xui.get_server_info()['streamSettings'])

        settings = stream_settings['realitySettings']['settings']

        client_config = {
            "ps": db_client.id,
            "add": config.get_server_hostname(),
            "port": "443",
            "id": db_client.id
        }

        client_data = {
            "pbk": settings['publicKey'],
            "security": "reality",
            "type": "tcp",
            "sni": "dl.google.com",
            "spx": "/",
            "sid": "deced1f3",
            "fp": "firefox"
        }

        conn_str = config_generator("vless", client_config, client_data)

        return ClientDTO(**{'id': db_client.id, 'conn_str': conn_str})

    def create(self, user_id: Optional[str] = None, comment: Optional[str] = None) -> str:
        client_id = self.xui.create_client(user_id)
        self.client_repo.create(client_id, user_id, comment)
        return client_id

    def delete(self, client_id: str) -> bool:
        self.client_repo.delete(client_id)
        self.xui.delete_client(client_id)
        return True
