from typing import Optional, List, Dict

from src.data.repo.user import User as UserRepo
from src.data.repo.clientconfig import ClientConfig as ClientRepo
from src.logic.models.user import User as UserDTO


class User:
    def __init__(self):
        self.user_repo = UserRepo()
        self.client_repo = ClientRepo()
        return

    def get_many(self, offset: int = 0, limit: int = 20) -> List[UserDTO]:
        return self.user_repo.get_many(offset, limit)

    def allowed_to_create_client(self, user_id: str) -> bool:
        user = self.user_repo.get(user_id)
        if user is None:
            return False

        return self.client_repo.count_by_user(user_id) < user.limit

    def get(self, user_id: str) -> Optional[UserDTO]:
        return self.user_repo.get(user_id)

    def create(self, user_id: str, limit: int) -> bool:
        if self.user_repo.get(user_id) is not None:
            return False

        self.user_repo.create(user_id, limit)
        return True

    def delete(self, user_id: str) -> bool:
        return self.user_repo.delete(user_id)

