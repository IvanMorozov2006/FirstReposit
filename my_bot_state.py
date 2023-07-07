from Config import Token

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=Token)
dp = Dispatcher(bot)

url = 'https://api.thecatapi.com/v1/images/search'

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет, как тебя зовут? :)")

@dp.message_handler()
async def repeat_message(message: types.Message):
    await message.answer(message['text'])


executor.start_polling(dp, skip_updates=True)