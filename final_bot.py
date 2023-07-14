from aiogram import Bot, Dispatcher, types, executor
from Config import Token
import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


def update_game_board(row, col, player, game_board):
    game_board[row][col] = player
    return game_board


def is_game_over(game_board):
    for row in game_board:
        if row.count(row[0]) == len(row) and row[0] != " ":
            if row[0] == 'X':
                return 'X'
            else:
                return 'O'

    for col in range(len(game_board[0])):
        if all(game_board[row][col] == game_board[0][col] and game_board[0][col] != " " for row in range(len(game_board))):
            if game_board[0][col] == 'X':
                return 'X'
            else:
                return 'O'

    if (game_board[0][0] == game_board[1][1] == game_board[2][2] != " ") or (
            game_board[0][2] == game_board[1][1] == game_board[2][0] != " "):
        if game_board[1][1] == 'X':
            return 'X'
        else:
            return 'O'

    check = False
    for i in range(3):
        if ' ' in game_board[i]:
            check = True
            break
    if check == False:
        return ' '
    return 'no'


@dp.callback_query_handler(lambda query: query.data.startswith('move'), state='*')
async def make_move(callback_query: types.CallbackQuery, state: FSMContext):
    row, col = map(int, callback_query.data.split(':')[1].split(','))
    data = await state.get_data()
    s = data['s']
    game_board = data['game_board']
    if s == 'no':
        if game_board[row][col] == ' ':
            player = "X"
            bot_player = "O"

            game_board = update_game_board(row, col, player, game_board)
            check = False
            for i in range(3):
                if ' ' in game_board[i]:
                    check = True
                    break

            if check:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
                while game_board[row][col] != ' ':
                    row = random.randint(0, 2)
                    col = random.randint(0, 2)
                game_board = update_game_board(row, col, bot_player, game_board)

            markup = types.InlineKeyboardMarkup(row_width=3)
            for i in range(3):
                buttons_row = []
                for j in range(3):
                    button_text = game_board[i][j]
                    button_callback = f"move:{i},{j}"
                    buttons_row.append(types.InlineKeyboardButton(text=button_text, callback_data=button_callback))
                markup.row(*buttons_row)
            await state.update_data(game_board=game_board)
            await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)

            s = is_game_over(game_board)
            await state.update_data(s=s)
            if s != 'no':
                winner = s
                if winner == " ":
                    message = "Упс, ничья... Попробуй еще раз! :)"
                else:
                    message = f"Игрок {winner} победил!"
                await bot.send_message(callback_query.message.chat.id, message)
        else:
            await bot.send_message(callback_query.message.chat.id, 'Это место уже занято!')
    else:
        await bot.send_message(callback_query.message.chat.id, 'Нельзя, игра уже закончилась!')


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.update_data(game_board=[[' '] * 3 for i in range(3)])
    await state.update_data(s='no')
    data = await state.get_data()
    game_board = data['game_board']
    markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(3):
        buttons_row = []
        for j in range(3):
            button_text = game_board[i][j]
            button_callback = f"move:{i},{j}"
            buttons_row.append(types.InlineKeyboardButton(text=button_text, callback_data=button_callback))
        markup.row(*buttons_row)

    await bot.send_message(message.chat.id, "Добро пожаловать в бота Крестики-Нолики!\nМожешь начать играть :)", reply_markup=markup)


executor.start_polling(dp, skip_updates=True)

