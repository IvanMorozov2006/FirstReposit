from Config import Token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import random


bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
b = KeyboardButton("Готов")
ready_keyboard=ReplyKeyboardMarkup(resize_keyboard=True).insert(b)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.set_state('Ready')
    await message.answer('Когда будете готовы, нажмите "Готов"', reply_markup=ready_keyboard)

@dp.message_handler(state='Ready')
async def ready(message: types.Message, state: FSMContext):
    if message.text == 'Готов':
        await state.set_state('Play')
        await state.update_data(game=[[' ']*3 for i in range(3)])
        data = await state.get_data()
        x = random.randint(0, 1)
        await state.update_data(x=x)
        await bot.send_message(message.from_id, 'Твой ход')
        if x == 1:
            await message.answer(draw_board(data['game']), reply_markup=ReplyKeyboardRemove)
        else:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            mass = data['game']
            mass[i][j] = 'X'
            await message.answer(draw_board(data['game']), reply_markup=ReplyKeyboardRemove)
    else:
        await message.answer('Когда будете готовы, нажмите "Готов".')


@dp.message_handler(state='play')
async def play(message: types.Message, state: FSMContext):
    data = await state.get_data()
    hod = data['x']



def draw_board(game_state):
    """Draws the current game board"""
    board = 'Доска:' + '\n'
    for i in range(3):
        for j in range(3):
            if j == 0:
                board += game_state[i][j]
            if j == 1:
                board += ' | ' + game_state[i][j] + ' | '
            if j == 2:
                board += game_state[i][j] + '\n'
    return board


def check_winner(game_state):
    """Checks if there is a winner"""
    # Check rows
    for row in game_state:
        if row[0] == row[1] == row[2] != ' ':
            return True

    # Check columns
    for col in range(3):
        if game_state[0][col] == game_state[1][col] == game_state[2][col] != ' ':
            return True

    # Check diagonals
    if game_state[0][0] == game_state[1][1] == game_state[2][2] != ' ':
        return True
    if game_state[0][2] == game_state[1][1] == game_state[2][0] != ' ':
        return True

    return False


def check_draw(game_state):
    """Checks if the game is a draw"""
    for row in game_state:
        if ' ' in row:
            return False
    return True


executor.start_polling(dp, skip_updates=True)
