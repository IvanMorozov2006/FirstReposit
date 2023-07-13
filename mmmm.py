from aiogram import Bot, Dispatcher, types, executor
import asyncio
from Config import Token

# Initialize bot and dispatcher
bot = Bot(token=Token)
dp = Dispatcher(bot)

# Define the game state and current player
game_state = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

# Function to draw the game board
def draw_board():
    board = ""
    for row in game_state:
        board += " | ".join(row)
        board += "\n"
    return board.strip()

# Function to switch players
def switch_player():
    global current_player
    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'

# Function to check for a winner or draw
def check_winner():
    # Check rows
    for row in game_state:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    # Check columns
    for col in range(3):
        if game_state[0][col] == game_state[1][col] == game_state[2][col] != ' ':
            return game_state[0][col]
    # Check diagonals
    if game_state[0][0] == game_state[1][1] == game_state[2][2] != ' ':
        return game_state[0][0]
    if game_state[0][2] == game_state[1][1] == game_state[2][0] != ' ':
        return game_state[0][2]
    # Check for a draw
    if all(game_state[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'draw'
    # No winner or draw
    return None

# Function to reset the game state
def reset_game():
    global game_state, current_player
    game_state = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    reset_game()
    await message.reply("Let's play tic-tac-toe!\n" + draw_board())

# Handler for user's moves
@dp.callback_query_handler(lambda c: c.data in ['0', '1', '2', '3', '4', '5', '6', '7', '8'])
async def make_move(callback_query: types.CallbackQuery):
    global game_state, current_player
    move = int(callback_query.data)
    row = move // 3
    col = move % 3
    if game_state[row][col] == ' ':
        game_state[row][col] = current_player
        winner = check_winner()
        if winner:
            await callback_query.message.reply(f"{winner} wins!nn" + draw_board())
            reset_game()
        else:
            switch_player()
            await callback_query.message.reply(draw_board())
    else:
        await callback_query.answer("Invalid move!")

# Main function to start the bot
executor.start_polling(dp, skip_updates=True)