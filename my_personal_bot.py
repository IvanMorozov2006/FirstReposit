from __future__ import annotations

import asyncio

from Config import Token

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в бота Крестики-Нолики!\nДля начала игры нажмите /newgame :)")
    await state.set_state("newgame")

@dp.callback_query_handler(commands=['newgame'], state="newgame")
async def newgame_message(callback_query: types.CallbackQuery, message: types.Message, state: FSMContext):
    await message.answer("Ваш ход")
    await callback_query.answer('+1')

