from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logic import Admin, Client, User
from src.presentation.callbacks import ClientCallback

items_per_page = 7

admin_menu = [
    [InlineKeyboardButton(text="➕ Добавить юзера", callback_data="add_client"),
     InlineKeyboardButton(text="❌ Удалить юзера", callback_data="delete_client")],
    [InlineKeyboardButton(text="📃 Список юзеров", callback_data="user_list")]
]

client_menu = [
    [InlineKeyboardButton(text="📃 Мои конфигурации", callback_data="conf_list")],
    [InlineKeyboardButton(text="🔧 Запросить конфигурацию", callback_data="create_config")],
    [InlineKeyboardButton(text="🔍 Инструкции", callback_data="get_instructions")]
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


class Pagination(StatesGroup):
    showing_items = State()


class PageCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    page: int


class EmailCallbackFactory(CallbackData, prefix="fabemail"):
    email: str


async def get_page_keyboard(emails_on_page: list, page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    for email in emails_on_page:
        builder.row(InlineKeyboardButton(text=email, callback_data=EmailCallbackFactory(email=email).pack()))
    if total_pages != 1:
        builder.row(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="ignore"))
    if page > 1:
        builder.add(InlineKeyboardButton(text="<<", callback_data=PageCallbackFactory(action="prev", page=page).pack()))
    if page < total_pages:
        builder.add(InlineKeyboardButton(text=">>", callback_data=PageCallbackFactory(action="next", page=page).pack()))
    builder.row(InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="main_menu"))
    return builder.as_markup()


async def show_items_page(clbck: PageCallbackFactory, page: int = 1):
    user_id = clbck.from_user.id
    emails = Client().get_by_user(user_id)
    if len(emails) == 0:
        return await clbck.message.answer("У вас пока нет туннелей", reply_markup=iexit_kb)
    total_pages = len(emails) // items_per_page + (len(emails) % items_per_page > 0)
    text = f"Выберите туннель:"
    start = (page - 1) * items_per_page
    end = start + items_per_page
    emails_on_page = emails[start:end]
    keyboard = await get_page_keyboard(emails_on_page, page, total_pages)
    await clbck.message.answer(text, reply_markup=keyboard)
