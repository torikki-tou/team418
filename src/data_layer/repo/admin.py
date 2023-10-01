import os
from typing import List

from src.data_layer.models.admin import Admin as AdminDTO


class Admin:
    def __init__(self):
        admins: str = os.environ['ADMIN_IDS']
        self.admins = admins.split(',')
        return

    def get_all(self) -> List[AdminDTO]:
        return [AdminDTO(**{'id': admin_id}) for admin_id in self.admins]
