from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    AIORateLimiter,
    filters,
    CallbackQueryHandler,
)

import config
import telegram_utils as tu


def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.worker)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .build()
    )

    application.add_handler(CommandHandler("start", tu.start_handle))
    #application.add_handler(CommandHandler("broadcast", tu.broadcast_handle))
    application.add_handler(CommandHandler("mode", tu.show_modes_handle))

    application.add_handler(MessageHandler(filters.TEXT, tu.message_handle))
    application.add_handler(MessageHandler(filters.PHOTO, tu.photo_handle))
    application.add_handler(
        CallbackQueryHandler(tu.show_modes_callback_handle, pattern="^show_modes")
    )
    application.add_handler(
        CallbackQueryHandler(tu.set_mode_handle, pattern="^set_mode")
    )

    # start the bot
    application.run_polling()


if __name__ == "__main__":
    run_bot()
