from typing import List

from src.data.models.admin import Admin as AdminDTO

from src.infrastracture.config import config
from src.infrastracture.logger import logger


class Admin:
    def __init__(self):
        admins = config.get_admins_ids()
        if not admins:
            logger.critical('no admin ids found')
        self.__admins: List[str] = admins
        return

    def get_all(self) -> List[AdminDTO]:
        return [AdminDTO(**{'id': admin_id}) for admin_id in self.__admins]
