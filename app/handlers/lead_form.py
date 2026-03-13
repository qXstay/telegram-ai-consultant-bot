from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.handlers.manager_handoff import send_lead_to_manager
from app.handlers.start import show_main_menu
from app.keyboards import (
    FSM_BACK,
    FSM_CANCEL,
    MAIN_MENU_LEAD,
    get_form_navigation_keyboard,
    get_main_menu_keyboard,
    get_task_keyboard,
)
from app.states import LeadForm
from app.storage import save_lead


router = Router()
logger = logging.getLogger(__name__)


async def start_lead_form(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.name)
    await message.answer(
        "Оставим короткую заявку. Как к вам можно обращаться?",
        reply_markup=get_form_navigation_keyboard(include_back=False),
    )


async def cancel_lead_form(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Хорошо, заявку остановил. Когда будет удобно, можно вернуться к диалогу из главного меню.",
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext) -> None:
    await cancel_lead_form(message, state)


@router.message(F.text == MAIN_MENU_LEAD)
async def lead_from_menu(message: Message, state: FSMContext) -> None:
    await start_lead_form(message, state)


@router.callback_query(F.data == "faq_action:lead")
async def lead_from_faq(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if callback.message is not None:
        await start_lead_form(callback.message, state)


@router.message(LeadForm.name, F.text == FSM_CANCEL)
@router.message(LeadForm.contact, F.text == FSM_CANCEL)
@router.message(LeadForm.task, F.text == FSM_CANCEL)
@router.message(LeadForm.comment, F.text == FSM_CANCEL)
async def cancel_from_form(message: Message, state: FSMContext) -> None:
    await cancel_lead_form(message, state)


@router.message(LeadForm.contact, F.text == FSM_BACK)
async def back_to_name(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.name)
    await message.answer(
        "Вернулись на шаг назад. Как к вам обращаться?",
        reply_markup=get_form_navigation_keyboard(include_back=False),
    )


@router.message(LeadForm.task, F.text == FSM_BACK)
async def back_to_contact(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.contact)
    await message.answer(
        "Подскажите удобный контакт: телефон, Telegram или email.",
        reply_markup=get_form_navigation_keyboard(),
    )


@router.message(LeadForm.comment, F.text == FSM_BACK)
async def back_to_task(message: Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.task)
    await message.answer(
        "Уточните, какой сценарий хотите запустить.",
        reply_markup=get_task_keyboard(),
    )


@router.message(LeadForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.text is None or not message.text.strip():
        await message.answer("Напишите имя текстом, чтобы я корректно оформил заявку.")
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(LeadForm.contact)
    await message.answer(
        "Подскажите удобный контакт: телефон, Telegram или email.",
        reply_markup=get_form_navigation_keyboard(),
    )


@router.message(LeadForm.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    if message.text is None or not message.text.strip():
        await message.answer("Укажите контакт текстом: например, телефон, @username или email.")
        return

    await state.update_data(contact=message.text.strip())
    await state.set_state(LeadForm.task)
    await message.answer(
        "Что именно хотите запустить? Можно выбрать вариант ниже или написать свой.",
        reply_markup=get_task_keyboard(),
    )


@router.message(LeadForm.task)
async def process_task(message: Message, state: FSMContext) -> None:
    if message.text is None or not message.text.strip():
        await message.answer("Коротко опишите задачу текстом, чтобы я передал ее менеджеру.")
        return

    await state.update_data(task=message.text.strip())
    await state.set_state(LeadForm.comment)
    await message.answer(
        "Есть ли детали, сроки или пожелания, которые важно учесть?",
        reply_markup=get_form_navigation_keyboard(),
    )


@router.message(LeadForm.comment)
async def process_comment(message: Message, state: FSMContext, manager_chat_id: int) -> None:
    if message.text is None or not message.text.strip():
        await message.answer("Напишите комментарий текстом. Если деталей пока нет, можно так и указать.")
        return

    data = await state.update_data(comment=message.text.strip())

    user = message.from_user
    if user is None:
        logger.error("Message without from_user while saving lead")
        await state.clear()
        await message.answer(
            "Не удалось сохранить заявку. Попробуйте еще раз чуть позже.",
            reply_markup=get_main_menu_keyboard(),
        )
        return

    save_lead(
        telegram_user_id=user.id,
        username=user.username,
        name=data["name"],
        contact=data["contact"],
        task=data["task"],
        comment=data["comment"],
    )

    try:
        await send_lead_to_manager(
            bot=message.bot,
            manager_chat_id=manager_chat_id,
            name=data["name"],
            contact=data["contact"],
            task=data["task"],
            comment=data["comment"],
        )
    except Exception:
        logger.exception("Lead saved, but manager handoff failed for user %s", user.id)
        await state.clear()
        await message.answer(
            "Заявку сохранил, но сейчас не удалось передать ее менеджеру автоматически. "
            "Попробуйте повторить отправку немного позже.",
            reply_markup=get_main_menu_keyboard(),
        )
        return

    await state.clear()
    await message.answer(
        "Спасибо. Заявка принята, менеджер изучит детали и свяжется с вами по указанному контакту.",
        reply_markup=get_main_menu_keyboard(),
    )


__all__ = ["router", "start_lead_form"]
