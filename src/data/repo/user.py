from typing import Optional, List

from src.data.models.user import User as UserDTO
from src.infrastracture.db import db


class User:
    def __init__(self):
        self.__con = db.get_connection()
        self.__create_user_table()
        return

    def get_many(self, offset: int = 0, limit: int = 20) -> List[UserDTO]:
        query = '''
        SELECT * FROM users OFFSET ? LIMIT ?
        '''

        res = self.__con.cursor().execute(
            query,
            (offset, limit)
        ).fetchall()

        return [UserDTO(**{'id': e[0], 'limit': e[1]}) for e in res]

    def get(self, user_id: str) -> Optional[UserDTO]:
        query = '''
        SELECT * FROM users WHERE id = ?
        '''

        res = self.__con.cursor().execute(query, (user_id,)).fetchone()

        if res is None:
            return None

        return UserDTO(**{'id': res[0], 'limit': res[1]})

    def create(self, user_id: str, limit: int) -> None:
        query = '''
        INSERT OR REPLACE INTO users VALUES (?, ?)
        '''

        self.__con.cursor().execute(query, (user_id, limit))

        self.__con.commit()
        return

    def delete(self, user_id: str) -> bool:
        query = '''
        DELETE FROM users WHERE id = ?
        '''

        self.__con.cursor().execute(query, (user_id,))

        self.__con.commit()
        return True

    def __create_user_table(self):
        self.__con.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
               ID        TEXT PRIMARY KEY NOT NULL, 
               CFG_LIMIT INT              NOT NULL
               );
               '''
        )

        self.__con.commit()
