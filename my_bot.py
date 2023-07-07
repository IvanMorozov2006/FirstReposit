from Config import Token

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=Token)
dp = Dispatcher(bot)

user_id = []

url = 'https://api.thecatapi.com/v1/images/search'

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    """Обработчик сообщений"""
    await message.answer("Добро пожалоовать в бота")

@dp.message_handler(commands=['get_cat'])
async def send_cat(message: types.Message):
    response = requests.get(url).json()
    url_cat = response[0]['url']
    await message.answer_photo(url_cat)

@dp.message_handler()
async def repeat_message(message: types.Message):
    await message.answer(message['text'])


executor.start_polling(dp, skip_updates=True)