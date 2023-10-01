from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    typing_telegram_id = State()
    typing_limit = State()


class Del(StatesGroup):
    typing_telegram_id = State()


class GenConf(StatesGroup):
    typing_conf_id = State()


class DelConf(StatesGroup):
    typing_conf_id = State()
