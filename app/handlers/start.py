from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import (
    BACK_TO_MENU,
    MAIN_MENU_MANAGER,
    MAIN_MENU_SERVICES,
    get_main_menu_keyboard,
    get_manager_actions_keyboard,
    get_services_actions_keyboard,
)


router = Router()


START_TEXT = (
    "Здравствуйте!\n"
    "Я AI-консультант. Помогу быстро сориентироваться по услугам, срокам и формату запуска.\n"
    "Могу показать подходящие сценарии, ответить на частые вопросы и помочь оставить заявку."
)

SERVICES_TEXT = (
    "<b>Сценарии, которые можно запустить в Telegram</b>\n\n"
    "1. <b>Консультант по услугам и заявкам</b>\n"
    "Помогает клиенту быстро понять формат работы, снять типовые вопросы и оставить обращение.\n\n"
    "2. <b>Ассистент по базе знаний</b>\n"
    "Подходит для команд, которым важно быстро отвечать по регламентам, продукту или внутренним материалам.\n\n"
    "3. <b>Бот для записи и напоминаний</b>\n"
    "Удобен для консультаций, встреч, сервиса и других сценариев с подтверждением записи.\n\n"
    "4. <b>Бот с оплатой или подпиской</b>\n"
    "Используется для продажи доступа, подписных продуктов и цифровых услуг внутри Telegram."
)

MANAGER_TEXT = (
    "Если удобнее продолжить общение с менеджером, оставьте короткую заявку.\n"
    "Я аккуратно передам контакт и задачу, чтобы вам ответили уже предметно."
)


async def show_main_menu(message: Message, *, clear_state: FSMContext | None = None) -> None:
    if clear_state is not None:
        await clear_state.clear()

    await message.answer(START_TEXT, reply_markup=get_main_menu_keyboard())


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await show_main_menu(message, clear_state=state)


@router.message(F.text == MAIN_MENU_SERVICES)
async def services_handler(message: Message) -> None:
    await message.answer(SERVICES_TEXT, reply_markup=get_services_actions_keyboard())


@router.message(F.text == MAIN_MENU_MANAGER)
async def manager_handler(message: Message) -> None:
    await message.answer(MANAGER_TEXT, reply_markup=get_manager_actions_keyboard())


@router.message(F.text == BACK_TO_MENU)
async def back_to_menu_handler(message: Message, state: FSMContext) -> None:
    await show_main_menu(message, clear_state=state)


__all__ = [
    "router",
    "show_main_menu",
    "START_TEXT",
]
