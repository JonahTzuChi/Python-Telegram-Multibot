from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    AIORateLimiter,
)

import config
import telegram_utils as tu

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.master)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .build()
    )
    
    application.add_handler(CommandHandler("start", tu.start_handle))

    # start the bot
    application.run_polling()


if __name__ == "__main__":
    run_bot()