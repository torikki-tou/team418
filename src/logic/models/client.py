from pydantic import BaseModel


class Client(BaseModel):
    id: str
    conn_str: str
