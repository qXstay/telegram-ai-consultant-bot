from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.faq_data import get_faq_item, load_faq_items
from app.handlers.start import show_main_menu
from app.keyboards import MAIN_MENU_FAQ, get_faq_answer_keyboard, get_faq_keyboard


router = Router()


FAQ_INTRO_TEXT = (
    "Собрал частые вопросы по запуску Telegram-бота. "
    "Выберите нужный пункт, и я коротко поясню по делу."
)


async def show_faq_list(target: Message) -> None:
    faq_items = load_faq_items()
    await target.answer(FAQ_INTRO_TEXT, reply_markup=get_faq_keyboard(faq_items))


@router.message(F.text == MAIN_MENU_FAQ)
async def faq_menu_handler(message: Message) -> None:
    await show_faq_list(message)


@router.callback_query(F.data == "faq:menu")
async def faq_menu_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is not None:
        await show_main_menu(callback.message)


@router.callback_query(F.data.startswith("faq:"))
async def faq_answer_callback(callback: CallbackQuery) -> None:
    if callback.message is None:
        await callback.answer()
        return

    faq_id = callback.data.split(":", maxsplit=1)[1]
    item = get_faq_item(faq_id)
    await callback.answer()

    if item is None:
        await callback.message.answer("Не удалось открыть ответ. Попробуйте выбрать вопрос еще раз.")
        await show_faq_list(callback.message)
        return

    answer_text = f"<b>{item['question']}</b>\n\n{item['answer']}"
    await callback.message.edit_text(answer_text, reply_markup=get_faq_answer_keyboard())


@router.callback_query(F.data == "faq_action:list")
async def faq_list_callback(callback: CallbackQuery) -> None:
    if callback.message is None:
        await callback.answer()
        return

    await callback.answer()
    await callback.message.edit_text(
        FAQ_INTRO_TEXT,
        reply_markup=get_faq_keyboard(load_faq_items()),
    )


@router.callback_query(F.data == "faq_action:menu")
async def faq_action_menu_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.message is not None:
        await show_main_menu(callback.message)
