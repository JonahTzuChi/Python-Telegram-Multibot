import telegram
from telegram import (
    Update,
    User,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    AIORateLimiter,
    filters,
)
from telegram.constants import ParseMode, ChatAction

import config
import re

HELP_MESSAGE = """Commands:
/help – Show help
/quit – Quit
"""

async def sendMessage(bot, target_id, message):
    res = await bot.sendMessage(chat_id=target_id, text=message)

async def start_handle(update: Update, context: CallbackContext):
    USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    # Race condition are not handled
    with open("../static/members.txt", "a") as writer:
        writer.write(f"{USER_ID},{USERNAME},{1}\n")

    reply_text = f"Hi! {USERNAME} I'm master bot\n\n"
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

async def help_handle(update: Update, context: CallbackContext):
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.HTML)

async def quit_handle(update: Update, context: CallbackContext):
    USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    fin = open("../static/members.txt")
    data = data.read()
    fin.close()

    pattern = f"^{USER_ID},\w*,1$"
    replacement = f"^{USER_ID},{USERNAME},0"

    output = re.sub(pattern, replacement, data)

    with open("../static/members.txt") as writer:
        writer.write(output)

    reply_text = "Successfully quit from this program"
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
