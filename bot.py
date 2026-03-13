from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import load_config
from app.handlers import faq_router, lead_form_router, start_router
from app.storage import init_db


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


async def main() -> None:
    setup_logging()

    config = load_config()
    init_db()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()

    dispatcher.include_router(start_router)
    dispatcher.include_router(faq_router)
    dispatcher.include_router(lead_form_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, manager_chat_id=config.manager_chat_id)


if __name__ == "__main__":
    asyncio.run(main())
