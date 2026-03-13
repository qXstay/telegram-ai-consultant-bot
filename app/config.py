from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(slots=True)
class Config:
    bot_token: str
    manager_chat_id: int


def load_config() -> Config:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    manager_chat_id_raw = os.getenv("MANAGER_CHAT_ID", "").strip()

    if not bot_token:
        raise ValueError("BOT_TOKEN is required. Set it in the environment or .env file.")

    if not manager_chat_id_raw:
        raise ValueError("MANAGER_CHAT_ID is required. Set it in the environment or .env file.")

    try:
        manager_chat_id = int(manager_chat_id_raw)
    except ValueError as exc:
        raise ValueError("MANAGER_CHAT_ID must be an integer.") from exc

    return Config(bot_token=bot_token, manager_chat_id=manager_chat_id)
