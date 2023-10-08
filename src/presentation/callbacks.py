from aiogram.filters.callback_data import CallbackData

from src.logic.models.client import Client
from src.logic.models.user import User


class UserCallback(CallbackData, prefix="user"):
    tg_id: str
    clients: list[Client]


class ClientCallback(CallbackData, prefix="client"):
    client_id: str
