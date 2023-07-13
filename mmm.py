from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from Config import Token


# Initialize the bot and dispatcher

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


class TicTacToeGame(StatesGroup):
    PLAYING = State()


# Define the initial game state
game_state = [[' ']*3 for i in range(3)]

# Define the current player
current_player = 'X'


@dp.message_handler(commands = ["start"])
async def start_game(message: types.Message):
    """Handler for the /start command"""
    await message.reply("Welcome to Tic-Tac-Toe! To make a move, enter the row and column numbers (e.g., 1 2):")
    await message.reply(draw_board())
    await TicTacToeGame.PLAYING.set()


@dp.message_handler(state=TicTacToeGame.PLAYING)
async def make_move(message: types.Message, state: FSMContext):
    """Handler for the user's moves"""
    try:
        row, col = map(int, message.text.split())
        row -= 1
        col -= 1

        if game_state[row][col] == ' ':
            game_state[row][col] = current_player
            await message.reply(draw_board())

            if check_winner():
                await message.reply(f'Player {current_player} wins!')
                await reset_game(state)
            elif check_draw():
                await message.reply('Its a draw!')
                await reset_game(state)
            else:
                await switch_player(message)
                await message.reply(f'Current player: {current_player}')
        else:
            await message.reply('Invalid move! Please select an empty cell.')
    except ValueError:
        await message.reply('Invalid input! Please enter the row and column numbers (e.g., 1 2).')


async def switch_player(message: types.Message):
    """Switches the current player"""
    global current_player
    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'


def draw_board():
    """Draws the current game board"""
    board = ''
    for row in game_state:
        board += ' | '.join(row)
        board += '\n'
    return board


def check_winner():
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


def check_draw():
    """Checks if the game is a draw"""
    for row in game_state:
        if ' ' in row:
            return False
    return True


async def reset_game(state: FSMContext):
    """Resets the game state"""
    global game_state, current_player
    game_state = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    current_player = 'X'
    await state.finish()


executor.start_polling(dp, skip_updates=True)