from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logic import Admin, Client, User

admin_menu = [
    [InlineKeyboardButton(text="➕ Добавить юзера", callback_data="add_client"),
     InlineKeyboardButton(text="❌ Удалить юзера", callback_data="delete_client")]
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

admin_menu = InlineKeyboardMarkup(inline_keyboard=admin_menu)
client_menu = InlineKeyboardMarkup(inline_keyboard=client_menu)
instruction_menu = InlineKeyboardMarkup(inline_keyboard=instruction_menu)

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu")]])


# def make_config_list(user_id: str) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     client_ids = Client().get_by_user(user_id)
#     for client_id in client_ids:
#         builder.button(text=client_id, callback_data=cd_conf.)
#     return builder.as_markup()
#
#
# def make_handlers_list(user_id: str) -> list:
#
#     callbacks = []
#     for client_id in client_ids:
#         callbacks.append(f"btn_{client_id}")
#     return callbacks
