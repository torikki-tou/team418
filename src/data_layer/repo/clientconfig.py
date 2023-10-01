from typing import Optional, List, Dict

from src.data_layer.models.clientconfig import ClientConfig as ClientDTO
from src.data_layer.db.get import *


class ClientConfig:
    def __init__(self):
        self.db = get_client_db()
        return

    def get_by_user(self, user_id: str) -> List[ClientDTO]:
        res = self.db.cursor().execute('''
        SELECT * FROM clients WHERE user_id = ?
        ''', (user_id,)).fetchall()

        return [ClientDTO(**{'id': e[0], 'user_id': e[1]}) for e in res]

    def get(self, client_id: str) -> Optional[ClientDTO]:
        res = self.db.cursor().execute('''
        SELECT * FROM clients WHERE id = ?
        ''', (client_id,)).fetchone()

        if res is None:
            raise ClientNotFound

        return ClientDTO(**{'id': res[0], 'user_id': res[1]})

    def create(self, client_id: str, user_id: str) -> None:
        self.db.cursor().execute('''
        INSERT OR REPLACE INTO clients VALUES (?, ?)
        ''', (client_id, user_id))

        self.db.commit()
        return

    def delete(self, client_id: str) -> None:
        self.db.cursor().execute('''
        DELETE FROM clients WHERE id = ?
        ''', (client_id,))

        self.db.commit()
        return


class ClientNotFound(Exception):
    pass
