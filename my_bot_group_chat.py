import asyncio

from Config import Token

from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

users_id = []

@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await message.answer("Привет, как тебя зовут? :)")
    if message.from_user['id'] not in users_id:
        users_id.append(message.from_user['id'])
    await state.set_state("name")

@dp.message_handler(state="name")
async def name_message(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await message.answer(f"{name}, добро пожаловать в бота! А сколько тебе лет?")
    await state.set_state("age")

@dp.message_handler(state="age")
async def name_message(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data({"age": age})
    await message.answer(f"Отлично, тебе {age} лет! Теперь бот запущен")
    await state.set_state("groupEcho")

@dp.message_handler(state="groupEcho")
async def echo_message(message: types.Message, state: FSMContext):
    sent = []
    username = await state.get_data()
    for i in range(len(users_id)):
        if message.from_user.id != users_id[i]:
            sent.append(bot.send_message(users_id[i], f'{username["name"]} сказал: {message.text}'))
    await asyncio.gather(*sent)

executor.start_polling(dp, skip_updates=True)