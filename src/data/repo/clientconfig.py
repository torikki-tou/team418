from typing import Optional, List

from src.data.models.clientconfig import ClientConfig as ClientDTO
from src.infrastracture.db import db


class ClientConfig:
    def __init__(self):
        self.__con = db.get_connection()
        self.__create_clients_table()
        return

    def get_by_user(self, user_id: Optional[str], offset: int = 0, limit: int = 20) -> List[ClientDTO]:
        query = '''
        SELECT * FROM clients WHERE user_id = ? OFFSET ? LIMIT ?
        '''

        res = self.__con.cursor().execute(
            query,
            (user_id, offset, limit)
        ).fetchall()

        return [ClientDTO(**{'id': e[0], 'user_id': e[1]}) for e in res]

    def count_by_user(self, user_id: Optional[str]) -> int:
        query = '''
        SELECT count(*) FROM clients WHERE user_id = ?
        '''

        res = self.__con.cursor().execute(
            query,
            (user_id,)
        ).fetchone()

        return res[0]

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

    def create(self, client_id: str, user_id: Optional[str], comment: Optional[str]) -> None:
        query = '''
        INSERT OR REPLACE INTO clients VALUES (?, ?, ?)
        '''

        self.__con.cursor().execute(query, (
            client_id, user_id, comment
        ))

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
                USER_ID TEXT
                COMMENT TEXT
                );
            '''
        )

        self.__con.commit()
