from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Config import Token

# Initialize bot and dispatcher
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

# Tic-tac-toe game board
board = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]]

# Function to check if the game is over
def is_game_over():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True

    # Check if the board is full
    for row in board:
        if " " in row:
            return False

    return True

# Function to make a move
async def make_move(row, col, player):
    if board[row][col] == " ":
        board[row][col] = player
        return True
    else:
        return False

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Create the inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for row in range(3):
        for col in range(3):
            buttons.append(types.InlineKeyboardButton(text=" ", callback_data=f"{row},{col}"))
    keyboard.add(*buttons)

    await message.reply("Welcome to Tic-Tac-Toe! Click on the buttons to make your move.", reply_markup=keyboard)

# Handler for the InlineKeyboardButton clicks
@dp.callback_query_handler(lambda c: True)
async def make_move_handler(callback_query: types.CallbackQuery):
    row, col = callback_query.data.split(",")
    row = int(row)
    col = int(col)
    player = "X" if callback_query.from_user.id == 0 else "O"

    if await make_move(row, col, player):
        if is_game_over():
            winner = player
            if winner == "X":
                await callback_query.message.reply("Game over! X wins!")
            else:
                await callback_query.message.reply("Game over! O wins!")
            # Reset the game board
            board = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]
        else:
            # Switch players
            next_player = "O" if player == "X" else "X"
            await callback_query.message.reply(f"Player {next_player}'s turn.")

        # Update the inline keyboard
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        buttons = []
        for row in range(3):
            for col in range(3):
                buttons.append(types.InlineKeyboardButton(text=board[row][col], callback_data=f"{row},{col}"))
        keyboard.add(*buttons)
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=keyboard)
    else:
        await callback_query.message.reply("Invalid move. Please try again.")

executor.start_polling(dp, skip_updates=True)