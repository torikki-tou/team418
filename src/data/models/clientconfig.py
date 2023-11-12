from typing import Optional

from pydantic import BaseModel


class ClientConfig(BaseModel):
    id: str
    user_id: Optional[str]
    comment: Optional[str]
