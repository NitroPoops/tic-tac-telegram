import tictactoe
from random import randint
from typing import Union, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)


# token is a unique token to every bot that the creator of the bot has access to
# tokens should look something like this:
# 1234567:AAwrv19eH6nse59d8aELnc4
# put yours in TOKEN
TOKEN = ""


# function for the bot to reply "bye" when a user sends "/hey" to it
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update.effective_chat.id is the id of the chat that the user has sent the message in
    # this is so that the bot knows where to send the message to
    await context.bot.send_message(chat_id=update.effective_chat.id, text="bye")


# ---------------------


def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(
            0, header_buttons if isinstance(header_buttons, list) else [header_buttons]
        )
    if footer_buttons:
        menu.append(
            footer_buttons if isinstance(footer_buttons, list) else [footer_buttons]
        )
    return menu


game = tictactoe.TicTacToe()
chat_id = -1
message_id = -1


async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game, chat_id, message_id
    game = tictactoe.TicTacToe()
    chat_id = update.effective_chat.id

    button_list = []

    for i in range(3):
        for j in range(3):
            button_list.append(
                InlineKeyboardButton(game.board[i][j], callback_data=str(i * 3 + j))
            )

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))

    await context.bot.send_message(
        chat_id=chat_id, text="A new game has started!", reply_markup=reply_markup
    )

    message_id = update.effective_message.message_id + 1


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game, chat_id, message_id

    message = update.callback_query.message
    data = update.callback_query.data
    query_id = update.callback_query.id

    print(data)

    if message.chat_id == chat_id and message.message_id == message_id:
        available = game.getempty()
        if data in available:
            game.move("X", int(data))

            if game.checkwin():
                await context.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    text="You won!",
                )
            elif game.checkwin() == False and len(game.getempty()) == 0:
                await context.bot.edit_message_text(
                    chat_id=message.chat.id, message_id=message.message_id, text="Tie!"
                )
            else:
                available = game.getempty()
                bot_move = randint(0, len(available) - 1)
                game.move("O", int(available[bot_move]))
                if game.checkwin():
                    await context.bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                        text="You lose!",
                    )
                elif game.checkwin() == False and len(game.getempty()) == 0:
                    await context.bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                        text="Tie!",
                    )
                else:
                    button_list = []
                    for i in range(3):
                        for j in range(3):
                            button_list.append(
                                InlineKeyboardButton(
                                    game.board[i][j], callback_data=str(i * 3 + j)
                                )
                            )
                    reply_markup = InlineKeyboardMarkup(
                        build_menu(button_list, n_cols=3)
                    )
                    await context.bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                        text="Please make your move:",
                        reply_markup=reply_markup,
                    )
            await context.bot.answer_callback_query(query_id)

        else:
            print("filled")
            button_list = []
            for i in range(3):
                for j in range(3):
                    button_list.append(
                        InlineKeyboardButton(
                            game.board[i][j], callback_data=str(i * 3 + j)
                        )
                    )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            await context.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text="Please make your move:",
                reply_markup=reply_markup,
            )
            await context.bot.answer_callback_query(
                query_id, text="Please choose an empty space!"
            )

    else:
        if (
            message.text == "A new game has started!"
            or message.text == "Please make your move:"
        ):
            await context.bot.edit_message_text(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text="Game is no longer valid!",
            )


if __name__ == "__main__":
    # creates an entry point for the bot using its token
    app = ApplicationBuilder().token(TOKEN).build()

    # this creates a CommandHandler object
    # the first parameter is the command aka what the user writes after "/" to activate the command
    # the second parameter is the function written earlier
    start_handler = CommandHandler("hey", start)
    app.add_handler(start_handler)

    newgame_handler = CommandHandler("china", newgame)
    app.add_handler(newgame_handler)

    callbackhandler = CallbackQueryHandler(callback)
    app.add_handler(callbackhandler)

    # this starts the bot
    app.run_polling()
