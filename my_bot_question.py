from __future__ import annotations

"""ALL IS RUIN"""

import asyncio

from Config import Token

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import keyboards_question

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

waiting: set[int] = set()
connected: dict[int, int] = {}

@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await message.answer("Привет, как тебя зовут? :)")
    await state.set_state("name")

@dp.message_handler(state="name")
async def name_message(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await message.answer(f"{name}, добро пожаловать в бота! А сколько тебе лет?")
    await state.set_state("age")

@dp.message_handler(state="age")
async def age_message(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data({"age": age})
    await message.answer(f"Отлично, тебе {age} лет! Чтобы начать викторину, нажми /begin",)
    await state.set_state("begin")

@dp.message_handler(commands=['begin'], state="begin")
async def question_message(message: types.Message, state: FSMContext):
    await message.answer("Начинаем викторину!")
    await message.answer("Первый вопрос: Сколько букв в слове яблоко?", reply_markup=choose_answer1)
    await state.set_state("question1")

@dp.message_handler(commands=['begin'], state="begin")
async def question_message(message: types.Message, state: FSMContext):
    await message.answer("Начинаем викторину!")
    await message.answer("Первый вопрос: Сколько букв в слове яблоко?", reply_markup=choose_answer1)
    await state.set_state("question1")

executor.start_polling(dp, skip_updates=True)