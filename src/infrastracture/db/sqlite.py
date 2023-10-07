import sqlite3
from typing import Generator


class SQLiteCon:
    def __init__(self):
        self.__connection = sqlite3.connect('/db/db418.db')

    def get_connection(self) -> sqlite3.Connection:
        return self.__connection


sqlite_con = SQLiteCon()
