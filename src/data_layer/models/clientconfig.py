from pydantic import BaseModel


class ClientConfig(BaseModel):
    id: str
    user_id: str
