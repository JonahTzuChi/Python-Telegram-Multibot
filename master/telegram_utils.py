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

async def sendMessage(bot, target_id, message):
    res = await bot.sendMessage(chat_id=target_id, text=message)

async def start_handle(update: Update, context: CallbackContext):
    USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    reply_text = f"Hi! {USERNAME} I'm master bot\n\n"
    
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)