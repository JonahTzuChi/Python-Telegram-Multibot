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

def get_target_list():
    y = None
    with open("../static/members.txt", "r") as reader:
        y = reader.readlines()
    return y

async def sendMessage(bot, target_id, message):
    res = await bot.sendMessage(chat_id=target_id, text=message)

async def start_handle(update: Update, context: CallbackContext):
    USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    reply_text = f"Hi! {USERNAME} I'm worker bot\n\n"
    
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)


async def broadcast_handle(update: Update, context: CallbackContext):
    #USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    reply_text = f"Hi! {USERNAME}! Mission received!!!\n\n"
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

    target_list = get_target_list()
    await broadcast(target_list, "We hope that your enjoy our service :-)")

    await update.message.reply_text("Done!", parse_mode=ParseMode.HTML)

async def broadcast(target_list, content):
    master = telegram.Bot(token = config.master)
    for target in target_list:
        id, name = target.split(",")
        name = name.strip()
        reply_text = f'Dear {name},\n{content}'
        try:
            await sendMessage(master, int(id), message=reply_text)
        except:
            print(f"Failed: {id}:{name}")
