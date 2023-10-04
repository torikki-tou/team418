from typing import Optional, List

from src.data.models.clientconfig import ClientConfig as ClientDTO
from src.infrastracture.db import db


class ClientConfig:
    def __init__(self):
        self.__con = db.get_connection()
        self.__create_clients_table()
        return

    def get_by_user(self, user_id: str) -> List[ClientDTO]:
        query = '''
        SELECT * FROM clients WHERE user_id = ?
        '''

        res = self.__con.cursor().execute(
            query,
            (user_id,)
        ).fetchall()

        return [ClientDTO(**{'id': e[0], 'user_id': e[1]}) for e in res]

    def get(self, client_id: str) -> Optional[ClientDTO]:
        query = '''
        SELECT * FROM clients WHERE id = ?
        '''

        res = self.__con.cursor().execute(
            query, (client_id,)
        ).fetchone()

        if res is None:
            return None

        return ClientDTO(**{'id': res[0], 'user_id': res[1]})

    def create(self, client_id: str, user_id: str) -> None:
        query = '''
        INSERT OR REPLACE INTO clients VALUES (?, ?)
        '''

        self.__con.cursor().execute(query, (client_id, user_id))

        self.__con.commit()
        return

    def delete(self, client_id: str) -> None:
        query = '''
        DELETE FROM clients WHERE id = ?
        '''

        self.__con.cursor().execute(query, (client_id,))

        self.__con.commit()
        return

    def __create_clients_table(self):
        self.__con.execute(
            '''
            CREATE TABLE IF NOT EXISTS clients (
                ID      TEXT PRIMARY KEY NOT NULL, 
                USER_ID TEXT             NOT NULL
                );
            '''
        )

        self.__con.commit()
