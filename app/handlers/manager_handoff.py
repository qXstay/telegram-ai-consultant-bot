from __future__ import annotations

import logging

from aiogram import Bot

from app.utils import format_manager_lead_message


logger = logging.getLogger(__name__)


async def send_lead_to_manager(
    *,
    bot: Bot,
    manager_chat_id: int,
    name: str,
    contact: str,
    task: str,
    comment: str,
) -> None:
    message_text = format_manager_lead_message(
        name=name,
        contact=contact,
        task=task,
        comment=comment,
    )

    try:
        await bot.send_message(manager_chat_id, message_text)
    except Exception:
        logger.exception("Failed to send lead to manager chat %s", manager_chat_id)
        raise
