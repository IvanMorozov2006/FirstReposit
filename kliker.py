from __future__ import annotations

import asyncio

from Config import Token

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from keyboards_question import one_keyboard, two_keyboard

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

class States:
    KLIKER: str = 'KLIKER'

async def message_kliks(message: Message, state: FSMContext):
    kliks = (await state.get_data())["kliks"]

@dp.message_handler(commands=['start'],state='*')
async def process_start(message: types.Message, state: FSMContext):
    await message.answer("Начните кликать")
    await state.set_state(States.KLIKER)
    await message.answer("Нажми меня?", reply_markup=one_keyboard)
    await state.update_data(kliks=0)

@dp.callback_query_handler(lambda c: c.data == 'klik1', state='*')
async def process_klik(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Молодец! Но оно не работает...")
    await callback_query.message.edit_text()

@dp.callback_query_handler()
async def general_process(callback_query: types.CallbackQuery):
    await callback_query.answer("Что-то пошло не так...")

executor.start_polling(dp, skip_updates=True)