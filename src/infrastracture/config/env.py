import os
from typing import List


class EnvConfig:
    def __init__(self):
        self.__read_telegram_api_token()
        self.__read_admins_ids()
        self.__read_chat_ids()
        self.__read_default_max_configs()
        self.__read_engine_url()
        self.__read_engine_username()
        self.__read_server_hostname()
        self.__read_engine_password()

    def get_telegram_api_token(self, refresh: bool = False) -> str:
        if refresh:
            self.__read_telegram_api_token()

        return self.__telegram_api_token

    def get_admins_ids(self, refresh: bool = False) -> List[str]:
        if refresh:
            self.__read_admins_ids()

        return self.__admins_ids

    def get_chat_ids(self, refresh: bool = False) -> List[str]:
        if refresh:
            self.__read_chat_ids()

        return self.__chat_ids

    def get_default_max_configs(self, refresh: bool = False) -> int:
        if refresh:
            self.__read_default_max_configs()

        return self.__default_max_configs

    def get_engine_url(self, refresh: bool = False) -> str:
        if refresh:
            self.__read_engine_url()

        return self.__engine_url

    def get_server_hostname(self, refresh: bool = False) -> str:
        if refresh:
            self.__read_server_hostname()

        return self.__server_hostname

    def get_engine_username(self, refresh: bool = False) -> str:
        if refresh:
            self.__read_engine_username()

        return self.__engine_username

    def get_engine_password(self, refresh: bool = False) -> str:
        if refresh:
            self.__read_engine_password()

        return self.__engine_password

    def get_allow_chat_members(self, refresh: bool = False) -> bool:
        if refresh:
            self.__read_allow_chat_members()

        return self.__allow_chat_members

    def __read_telegram_api_token(self):
        self.__telegram_api_token: str = (os.environ.get('TELEGRAM_API_TOKEN')
                                          or None)

    def __read_admins_ids(self):
        admins_ids: str = os.environ.get('') or ''
        self.__admins_ids: List[str] = [admin_id.strip('@') for admin_id in
                                        (admins_ids.split(',') or [])]

    def __read_chat_ids(self):
        chat_ids: str = os.environ.get('') or ''
        self.__chat_ids: List[str] = chat_ids.split(',') or []

    def __read_default_max_configs(self):
        self.__default_max_configs: int = os.environ.get('') or 3

    def __read_engine_url(self):
        self.__engine_url: str = (os.environ.get('XUI_URL')
                                  or 'http://3x-ui:2053')

    def __read_server_hostname(self):
        self.__server_hostname: str = (os.environ.get('XUI_HOSTNAME')
                                       or '0.0.0.0')

    def __read_engine_username(self):
        self.__engine_username: str = os.environ.get('XUI_LOGIN') or 'admin'

    def __read_engine_password(self):
        self.__engine_password: str = os.environ.get('XUI_PASS') or 'admin'

    def __read_allow_chat_members(self):
        self.__allow_chat_members: bool = os.environ.get('ALLOW_CHAT_MEMBERS') or False


env_config = EnvConfig()
