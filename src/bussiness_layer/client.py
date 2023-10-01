from typing import Optional, List, Dict
import json

from pyxui.config_gen import config_generator

from src.bussiness_layer.models.client import Client as ClientDTO
from src.data_layer.repo.clientconfig import ClientConfig as ClientRepo
from src.data_layer.engine.xui import XUICli


class Client:
    def __init__(self):
        self.client_repo = ClientRepo()
        self.xui = XUICli()
        return

    def get_by_user(self, user_id: str) -> List[str]:
        return [cnf.id for cnf in self.client_repo.get_by_user(user_id)]

    def get(self, client_id: str) -> Optional[ClientDTO]:
        db_client = self.client_repo.get(client_id)

        if db_client is None:
            return None

        stream_settings = json.loads(self.xui.get_server()['streamSettings'])

        public_key = stream_settings['realitySettings']['settings']['publicKey']

        config = {
            "ps": db_client.id,
            "add": "testnamehost.ddns.net",
            "port": "443",
            "id": db_client.id
        }

        data = {
            "pbk": public_key,
            "security": "reality",
            "type": "tcp",
            "sni": "yahoo.com",
            "spx": "/",
            "sid": "deced1f3",
            "fp": "firefox"
        }

        conn_str = config_generator("vless", config, data)

        return ClientDTO(**{'id': db_client.id, 'conn_str': conn_str})

    def create(self, user_id: str) -> str:
        client_id = self.xui.create_client(user_id)
        self.client_repo.create(client_id, user_id)
        return client_id

    def delete(self, client_id: str) -> bool:
        self.client_repo.delete(client_id)
        self.xui.delete_client(client_id)
        return True
