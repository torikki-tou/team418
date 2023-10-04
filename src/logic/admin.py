from src.data.repo.admin import Admin as AdminRepo


class Admin:
    def __init__(self):
        self.data = AdminRepo()
        return

    def is_admin(self, telegram_id: str) -> bool:
        for admin in self.data.get_all():
            if admin.id == telegram_id:
                return True

        return False
