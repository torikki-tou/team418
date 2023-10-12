from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logic import Admin, Client, User
from src.presentation.callbacks import ClientCallback

admin_menu = [
    [InlineKeyboardButton(text="➕ Добавить юзера", callback_data="add_client"),
     InlineKeyboardButton(text="❌ Удалить юзера", callback_data="delete_client")],
    [InlineKeyboardButton(text="📃 Список юзеров", callback_data="user_list")]
]

client_menu = [
    [InlineKeyboardButton(text="📃 Мои конфигурации", callback_data="conf_list"),
     InlineKeyboardButton(text="🔧 Запросить конфигурацию", callback_data="create_config")],
    [InlineKeyboardButton(text="❌ Удалить Конфигурацию", callback_data="delete_config"),
     InlineKeyboardButton(text="🔍 Инструкции", callback_data="get_instructions")]
]
instruction_menu = [
    [InlineKeyboardButton(text="iOS", callback_data="instruction_ios"),
     InlineKeyboardButton(text="Android", callback_data="instruction_android")],
    [InlineKeyboardButton(text="MacOS", callback_data="instruction_macos"),
     InlineKeyboardButton(text="Windows", callback_data="instruction_windows")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]
config_sub_menu = [
    [InlineKeyboardButton(text="Запросить URI", callback_data="get_config")],
    [InlineKeyboardButton(text="Удалить конфигурацию", callback_data="delete_config")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]

user_sub_menu = [
    [InlineKeyboardButton(text="Изменить лимит", callback_data="change_limit")],
    [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]
]

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_menu)
client_menu = InlineKeyboardMarkup(inline_keyboard=client_menu)
instruction_menu = InlineKeyboardMarkup(inline_keyboard=instruction_menu)
config_sub_menu = InlineKeyboardMarkup(inline_keyboard=config_sub_menu)
user_sub_menu = InlineKeyboardMarkup(inline_keyboard=user_sub_menu)

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]])


def create_conf_list(username: str) -> InlineKeyboardMarkup():
    builder = InlineKeyboardBuilder()
    clients = Client().get_by_user(username)
    for client in clients:
        builder.button(
            text=client, callback_data=ClientCallback(client_id=client)
        )
    return builder.as_markup()
