import sqlite3

db_path = 'db418.db'


def get_user_db() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)

    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS users 
           (ID TEXT PRIMARY KEY     NOT NULL, 
           CFG_LIMIT            INT     NOT NULL);
           '''
    )

    return conn


def get_client_db() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)

    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS clients 
           (ID TEXT PRIMARY KEY     NOT NULL, 
           USER_ID            TEXT     NOT NULL);
           '''
    )

    return conn
