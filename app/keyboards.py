from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


MAIN_MENU_SERVICES = "Узнать услуги"
MAIN_MENU_FAQ = "Частые вопросы"
MAIN_MENU_LEAD = "Оставить заявку"
MAIN_MENU_MANAGER = "Связаться с менеджером"
BACK_TO_MENU = "Назад в меню"
FSM_CANCEL = "Отменить заявку"
FSM_BACK = "Назад"
FAQ_ASK_ANOTHER = "Задать другой вопрос"


TASK_SUGGESTIONS = [
    "FAQ и заявки в Telegram",
    "Бот по базе знаний",
    "Запись и напоминания",
    "Оплата / подписка",
]


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=MAIN_MENU_SERVICES),
        KeyboardButton(text=MAIN_MENU_FAQ),
    )
    builder.row(
        KeyboardButton(text=MAIN_MENU_LEAD),
        KeyboardButton(text=MAIN_MENU_MANAGER),
    )
    return builder.as_markup(resize_keyboard=True)


def get_services_actions_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=MAIN_MENU_LEAD))
    builder.row(KeyboardButton(text=BACK_TO_MENU))
    return builder.as_markup(resize_keyboard=True)


def get_manager_actions_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=MAIN_MENU_LEAD))
    builder.row(KeyboardButton(text=BACK_TO_MENU))
    return builder.as_markup(resize_keyboard=True)


def get_form_navigation_keyboard(*, include_back: bool = True) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if include_back:
        builder.row(
            KeyboardButton(text=FSM_BACK),
            KeyboardButton(text=FSM_CANCEL),
        )
    else:
        builder.row(KeyboardButton(text=FSM_CANCEL))

    return builder.as_markup(resize_keyboard=True)


def get_task_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for task in TASK_SUGGESTIONS:
        builder.row(KeyboardButton(text=task))
    builder.row(
        KeyboardButton(text=FSM_BACK),
        KeyboardButton(text=FSM_CANCEL),
    )
    return builder.as_markup(resize_keyboard=True)


def get_faq_keyboard(items: list[dict[str, str]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.row(
            InlineKeyboardButton(
                text=item["question"],
                callback_data=f"faq:{item['id']}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=BACK_TO_MENU, callback_data="faq:menu")
    )
    return builder.as_markup()


def get_faq_answer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=MAIN_MENU_LEAD, callback_data="faq_action:lead")
    )
    builder.row(
        InlineKeyboardButton(text=FAQ_ASK_ANOTHER, callback_data="faq_action:list")
    )
    builder.row(
        InlineKeyboardButton(text=BACK_TO_MENU, callback_data="faq_action:menu")
    )
    return builder.as_markup()
