from __future__ import  annotations

import asyncio

from Config import Token

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

button1 = KeyboardButton("чат 1 на 1")
button2 = KeyboardButton("групповой чат")

choose_chat = ReplyKeyboardMarkup(resize_keyboard=True).insert(button1).insert(button2)

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
    await message.answer(f"Отлично, тебе {age} лет! Как ты хочешь общаться?", reply_markup=choose_chat)
    await state.set_state("find")

@dp.message_handler(commands=['find'], state="find")
async def find_message(message: types.Message, state: FSMContext):
    await message.answer("Ищем собеседника...")
    waiting.add(message.from_user.id)
    while len(waiting) >= 2:
        user1_id = waiting.pop()
        user2_id = waiting.pop()

        await dp.current_state(chat=user1_id, user=user1_id).set_state("chatting")
        await dp.current_state(chat=user2_id, user=user2_id).set_state("chatting")

        connected[user1_id] = user2_id
        connected[user2_id] = user1_id

        await bot.send_message(chat_id=user1_id, text="Вы начали общаться")
        await bot.send_message(chat_id=user2_id, text="Вы начали общаться")

@dp.message_handler(state="chatting")
async def chatting_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chatmate_id = connected[user_id]
    await bot.send_message(chat_id=chatmate_id, text=message.text)

executor.start_polling(dp, skip_updates=True)