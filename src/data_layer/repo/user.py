from typing import Optional, List

from src.data_layer.models.user import User as UserDTO
from src.data_layer.db.get import *


class User:
    def __init__(self):
        self.db = get_user_db()
        return

    def get_all(self) -> List[UserDTO]:
        res = self.db.cursor().execute('''
        SELECT * FROM users
        ''').fetchall()

        return [UserDTO(**{'id': e[0], 'limit': e[1]}) for e in res]

    def get(self, user_id: str) -> Optional[UserDTO]:
        res = self.db.cursor().execute('''
        SELECT * FROM users WHERE id = ?
        ''', (user_id,)).fetchone()

        if res is None:
            return None

        return UserDTO(**{'id': res[0], 'limit': res[1]})

    def create(self, user_id: str, limit: int) -> None:
        self.db.cursor().execute('''
        INSERT OR REPLACE INTO users VALUES (?, ?)
        ''', (user_id, limit))

        self.db.commit()
        return

    def delete(self, user_id: str) -> bool:
        self.db.cursor().execute('''
        DELETE FROM users WHERE id = ?
        ''', (user_id,))

        self.db.commit()
        return True
