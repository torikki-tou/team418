from os import getenv

from aiogram.filters.callback_data import CallbackData

from src.logic import Admin, Client, User
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import flags

import src.presentation.kb as kb
import src.presentation.text as text
from src.presentation.callbacks import ClientCallback
from src.presentation.states import Gen, Del, GenConf, DelConf

router = Router()
admin_id = getenv("ADMIN_TELEGRAM_ID")

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()

    if msg.from_user.username == admin_id:
        await msg.answer(text.hello_admin, reply_markup=kb.admin_menu)
    else:
        await msg.answer(text.hello_clint, reply_markup=kb.client_menu)


@router.callback_query(F.data == "main_menu")
async def menu_handler(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text=text.main_menu, reply_markup=kb.admin_menu)
    else:
        await clbck.message.answer(text=text.main_menu, reply_markup=kb.client_menu)


@router.callback_query(F.data == "get_instructions")
async def get_instructions(clbck: CallbackQuery):
    await clbck.message.answer(text.instructions, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "add_client")
async def add_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text.client_id_await, reply_markup=kb.iexit_kb)
        await state.set_state(Gen().typing_telegram_id)


@router.message(Gen.typing_telegram_id)
async def get_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text
        await state.update_data(chosen_id=tg_id)
        await msg.answer(text.client_limit_await, reply_markup=kb.iexit_kb)
        await state.set_state(Gen().typing_limit)


@router.message(Gen.typing_limit)
async def get_limit(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        limit = msg.text
        if not limit.isnumeric():
            await state.clear()
            return await msg.answer(text.limit_error, reply_markup=kb.iexit_kb)
        else:
            limit = int(limit)
            user_data = await state.get_data()
            tg_id = user_data['chosen_id']
            User().create(user_id=tg_id, limit=limit)
            await state.clear()


@router.callback_query(F.data == "delete_client")
async def add_client(clbck: CallbackQuery, state: FSMContext):
    if clbck.from_user.username == admin_id:
        await clbck.message.answer(text.client_id_await, reply_markup=kb.iexit_kb)
        await state.set_state(Del().typing_telegram_id)


@router.message(Gen.typing_telegram_id)
async def delete_telegram_id(msg: Message, state: FSMContext):
    if msg.from_user.username == admin_id:
        tg_id = msg.text
        if not tg_id.isnumeric() or len(tg_id) != 9:
            await state.clear()
            return await msg.answer(text.telegram_id_error, reply_markup=kb.iexit_kb)
        else:
            User().delete(user_id=tg_id)
            await state.clear()


@router.callback_query(F.data == "create_config")
async def add_config(clbck: CallbackQuery):
    user_id = str(clbck.from_user.username)
    if User().get(user_id) is None:
        return await clbck.message.answer(text.user_not_defined, reply_markup=kb.iexit_kb)
    if not User().allowed_to_create_client(user_id):
        return await clbck.message.answer(text.user_limit_exited, reply_markup=kb.iexit_kb)
    client_id = Client().create(user_id=user_id)
    client = Client().get(client_id)
    uri = client.conn_str
    await clbck.message.answer(text=uri, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "delete_config")
async def delete_config(clbck: CallbackQuery, state: FSMContext):
    user_id = str(clbck.from_user.username)
    if User().get(user_id) is None:
        return await clbck.message.answer(text.user_not_defined, reply_markup=kb.iexit_kb)
    if not User().allowed_to_create_client(user_id):
        return await clbck.message.answer(text.user_limit_exited, reply_markup=kb.iexit_kb)
    await clbck.message.answer(text.config_id_await, reply_markup=kb.iexit_kb)
    await state.set_state(DelConf().typing_conf_id)


@router.message(DelConf.typing_conf_id)
async def delete_config_id(msg: Message, state: FSMContext):
    conf_id = msg.text
    if not conf_id.isalnum():
        await state.clear()
        return await msg.answer(text.config_id_error, reply_markup=kb.iexit_kb)
    else:
        client_id = msg.text
        if Client().get(client_id) is None:
            return await msg.answer(text.client_not_defined, reply_markup=kb.iexit_kb)
        Client().delete(client_id=client_id)
        await state.clear()
        await msg.answer(text.config_is_deleted, reply_markup=kb.iexit_kb)


@router.callback_query(ClientCallback.filter())
async def config_list(clbck: CallbackQuery):
    username = clbck.from_user.username
    await clbck.message.answer(text="Выбран конфиг ...")

