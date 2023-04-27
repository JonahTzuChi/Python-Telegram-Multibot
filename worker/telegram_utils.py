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


def file_handler(media):
    # raw file
    if type(media) != str:
        return media
    ext = media.split(".")
    # URL
    if "https://" in media or "http://" in media:
        return media
    if len(ext) > 1:
        # file_path, a complete path is required
        if ext[-1].lower() in ["jpg", "jpeg", "png", "mp4", "pdf"]:
            return open(media, "rb")
    # file_id
    print("file_id")
    return media


async def sendMessage(bot, target_id, message):
    res = await bot.sendMessage(chat_id=target_id, text=message)


async def sendPhoto(
    bot: telegram.Bot, target_id: str, photo: any, caption: str = None, return_id=True
):
    _photo = file_handler(photo)
    res = await bot.send_photo(
        chat_id=target_id,
        photo=_photo,
        caption=caption,
        allow_sending_without_reply=True,
        protect_content=False,
    )
    print(res)
    """
    # what I want to show here is photo[0]['file_id'] is equal to photo[1]['file_id']
    # and many more information are captured here
    Message(
        caption='###', 
        channel_chat_created=False, 
        chat=Chat(first_name='###', id=###, type=<ChatType.PRIVATE>, username='###'), 
        date=datetime.datetime(2023, 4, 26, 1, 14, 34, tzinfo=<UTC>), 
        delete_chat_photo=False, 
        from_user=User(first_name='###', id=###, is_bot=True, username='###_Bot'), 
        group_chat_created=False, 
        message_id=###, 
        photo=(
            PhotoSize(file_id='###', file_size=1431, file_unique_id='@@@@@@@@@@@@@@@@', height=90, width=62), 
            PhotoSize(file_id='###', file_size=7267, file_unique_id='$$$$$$$$$$$$$$$$', height=272, width=186)
        ), 
        supergroup_chat_created=False
    )
    """
    if return_id:
        return res["photo"][0]["file_id"]


async def start_handle(update: Update, context: CallbackContext):
    USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    reply_text = f"Hi! {USERNAME} I'm worker bot\n\n"

    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)


async def broadcast_handle(update: Update, context: CallbackContext):
    # USER_ID = update.message.from_user.id
    USERNAME = update.message.from_user.username

    reply_text = f"Hi! {USERNAME}! Mission received!!!\n\n"
    await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

    target_list = get_target_list()
    await broadcast(target_list, "We hope that your enjoy our service :-)")

    await update.message.reply_text("Done!", parse_mode=ParseMode.HTML)


async def broadcast(target_list, content):
    master = telegram.Bot(token=config.master)
    counter = 0
    for target in target_list:
        id, name, active = target.split(",")
        active = active.strip()
        if active == "0":
            continue
        reply_text = f"Dear {name},\n{content}"
        try:
            await sendMessage(master, int(id), message=reply_text)
            counter = counter + 1
        except:
            print(f"Failed: {id}:{name}")

    return counter


async def broadcast_photo(target_list, content):
    master = telegram.Bot(token=config.master)
    counter = 0
    for target in target_list:
        id, name, active = target.split(",")
        active = active.strip()
        if active == "0":
            continue
        reply_text = f"Dear {name}"
        res = await sendPhoto(master, int(id), photo=content, caption="broadcast photo", return_id=True)
        counter = counter + 1
        ''' 
        try:
            #await sendMessage(master, int(id), message=reply_text)
            res = await sendPhoto(master, int(id), photo=content, caption="broadcast photo", return_id=True)
            print(res)
            counter = counter + 1
        except:
            print(f"Failed: {id}:{name}")
        '''
    return counter


profiles = {75316412: {"mode": "Default"}}


def get_mode_menu(id):
    text = f"Current mode: {profiles[id]['mode']}\n"
    keyboard = [
        [InlineKeyboardButton("Broadcast", callback_data=f"set_mode|Broadcast")],
        [InlineKeyboardButton("Default", callback_data=f"set_mode|Default")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return text, reply_markup


async def show_modes_handle(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    text, reply_markup = get_mode_menu(user_id)
    await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )


async def show_modes_callback_handle(update: Update, context: CallbackContext):
    user_id = update.callback_query.from_user.id

    query = update.callback_query
    await query.answer()

    page_index = int(query.data.split("|")[1])
    if page_index < 0:
        return

    text, reply_markup = get_mode_menu(user_id)
    try:
        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )
    except telegram.error.BadRequest as e:
        if str(e).startswith("Message is not modified"):
            pass


async def set_mode_handle(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    mode = query.data.split("|")[1]
    user_id = update.callback_query.message.chat.id
    USERNAME = update.callback_query.message.chat.username

    profiles[user_id]["mode"] = mode

    await context.bot.send_message(
        user_id, f"Set {USERNAME} to {mode}", parse_mode=ParseMode.HTML
    )


async def message_handle(update: Update, context: CallbackContext, message=None):
    """
    Check user mode or service selected from db
    """
    user_id = update.message.from_user.id
    # USERNAME = update.message.from_user.username

    mode = profiles[user_id]["mode"]
    if mode == "Default":
        return

    _message = message or update.message.text
    target_list = get_target_list()
    counter = await broadcast(target_list, _message)

    await update.message.reply_text(
        f"Sent to {counter} accounts", parse_mode=ParseMode.HTML
    )


async def photo_handle(update: Update, context: CallbackContext, photo=None):
    """
    Check user mode or service selected from db
    """
    print("photo handle")
    user_id = update.message.from_user.id
    # USERNAME = update.message.from_user.username

    mode = profiles[user_id]["mode"]
    if mode == "Default":
        return

    _photo = photo or update.message.photo
    #print(update.message)
    #print(photo)
    target_list = get_target_list()
    print("file_id", _photo[0]["file_id"])
    counter = await broadcast_photo(target_list, _photo[0]["file_id"])

    await update.message.reply_text(
        f"Sent to {counter} accounts", parse_mode=ParseMode.HTML
    )

'''
(
    PhotoSize(
        file_id='AgACAgUAAxkBAAM_ZEo2IsMl6A7K4p1ELfEqtipBWMsAAg-5MRvt-FFWlh1qL4htjXsBAAMCAANzAAMvBA', 
        file_size=1848, 
        file_unique_id='AQADD7kxG-34UVZ4', 
        height=51, 
        width=90
    ), 
    PhotoSize(
        file_id='AgACAgUAAxkBAAM_ZEo2IsMl6A7K4p1ELfEqtipBWMsAAg-5MRvt-FFWlh1qL4htjXsBAAMCAANtAAMvBA', 
        file_size=29928, 
        file_unique_id='AQADD7kxG-34UVZy', 
        height=180, width=320
    ), 
    PhotoSize(
        file_id='AgACAgUAAxkBAAM_ZEo2IsMl6A7K4p1ELfEqtipBWMsAAg-5MRvt-FFWlh1qL4htjXsBAAMCAAN4AAMvBA', 
        file_size=142650, 
        file_unique_id='AQADD7kxG-34UVZ9', 
        height=450, width=800
    ), 
    PhotoSize(
        file_id='AgACAgUAAxkBAAM_ZEo2IsMl6A7K4p1ELfEqtipBWMsAAg-5MRvt-FFWlh1qL4htjXsBAAMCAAN5AAMvBA', 
        file_size=254997, 
        file_unique_id='AQADD7kxG-34UVZ-', 
        height=720, 
        width=1280
    )
)

'''

'''
Message(
    channel_chat_created=False, 
    chat=Chat(first_name='Jonah', id=75316412, type=<ChatType.PRIVATE>, username='jonah_yeoh'), 
    date=datetime.datetime(2023, 4, 27, 8, 48, 59, tzinfo=<UTC>), 
    delete_chat_photo=False, 
    from_user=User(first_name='Jonah', id=75316412, is_bot=False, language_code='en', username='jonah_yeoh'), 
    group_chat_created=False, 
    message_id=68, 
    photo=(
        PhotoSize(file_id='AgACAgUAAxkBAANEZEo2-zyPI3nnG1AOoWzZ6NKPVSEAAhG5MRvt-FFWdnH87kOlSWwBAAMCAANzAAMvBA', file_size=1255, file_unique_id='AQADEbkxG-34UVZ4', height=90, width=40), 
        PhotoSize(file_id='AgACAgUAAxkBAANEZEo2-zyPI3nnG1AOoWzZ6NKPVSEAAhG5MRvt-FFWdnH87kOlSWwBAAMCAANtAAMvBA', file_size=17759, file_unique_id='AQADEbkxG-34UVZy', height=320, width=144), 
        PhotoSize(file_id='AgACAgUAAxkBAANEZEo2-zyPI3nnG1AOoWzZ6NKPVSEAAhG5MRvt-FFWdnH87kOlSWwBAAMCAAN4AAMvBA', file_size=67162, file_unique_id='AQADEbkxG-34UVZ9', height=800, width=360), 
        PhotoSize(file_id='AgACAgUAAxkBAANEZEo2-zyPI3nnG1AOoWzZ6NKPVSEAAhG5MRvt-FFWdnH87kOlSWwBAAMCAAN5AAMvBA', file_size=116790, file_unique_id='AQADEbkxG-34UVZ-', height=1280, width=576)
    ), 
    supergroup_chat_created=False)
'''