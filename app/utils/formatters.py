from __future__ import annotations

from datetime import datetime
from html import escape


def format_manager_lead_message(
    *,
    name: str,
    contact: str,
    task: str,
    comment: str,
    created_at: str | None = None,
) -> str:
    safe_name = escape(name)
    safe_contact = escape(contact)
    safe_task = escape(task)
    safe_comment = escape(comment) if comment.strip() else "Без комментария"
    formatted_created_at = created_at or datetime.now().strftime("%d.%m.%Y %H:%M")

    return (
        "<b>Новая заявка из Telegram-бота</b>\n\n"
        f"<b>Имя:</b> {safe_name}\n"
        f"<b>Контакт:</b> {safe_contact}\n"
        f"<b>Задача:</b> {safe_task}\n"
        f"<b>Комментарий:</b> {safe_comment}\n\n"
        "<b>Источник:</b> AI-консультант Demo\n"
        f"<b>Дата/время:</b> {escape(formatted_created_at)}"
    )
