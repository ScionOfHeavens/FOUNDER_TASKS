import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F

from api_token import API_TOKEN
from quiz import QuizApp

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def delete_previous_message_buttons(func):
    async def wrapper(callback_query: types.CallbackQuery):
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None,  # Удаляем клавиатуру
        )
        await func(callback_query)
    return wrapper

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать квиз"))
    builder.add(types.KeyboardButton(text="Продолжить квиз"))
    builder.add(types.KeyboardButton(text="Статистика"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def get_next_question_query(user_id: int = 0, to_continue:bool=False) -> tuple[str, types.InlineKeyboardMarkup]:
    query_text, callback_data = await QuizApp.prepare_next_question(user_id, to_continue)
    callback_data: str
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
        text=query_text,
        callback_data=callback_data
    ))
    return builder.as_markup()

@dp.message(F.text=="Начать квиз" )
@dp.message(Command("quiz"))
async def start_quiz(message: types.Message):
    reply_markup = await get_next_question_query()
    await QuizApp.start_quiz(message.from_user.id)
    await message.answer(f"Давайте начнем квиз!", reply_markup=reply_markup)

@dp.message(F.text=="Продолжить квиз" )
@dp.message(Command("quiz"))
async def start_quiz(message: types.Message):
    reply_markup = await get_next_question_query(message.from_user.id, True)
    await message.answer(f"Давайте продолжим!", reply_markup=reply_markup)

@dp.message(F.text=="Статистика" )
@dp.message(Command("quiz"))
async def start_quiz(message: types.Message):
    msg = await QuizApp.get_statistics()
    await message.answer(msg)

@dp.callback_query(F.data.contains("QuestionQuery"))
@delete_previous_message_buttons
async def send_question_and_options(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    question, reply_markup = await QuizApp.play_card(user_id)
    await callback_query.message.answer(question, reply_markup=reply_markup)

@dp.callback_query(F.data.contains("Answer"))
@delete_previous_message_buttons
async def handle_answer(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    reply_msg = await QuizApp.check_answer(data, user_id)
    reply_markup = await get_next_question_query(user_id)
    await callback_query.message.answer(reply_msg, reply_markup=reply_markup)

@dp.callback_query(F.data.contains("FinishQuiz"))
@delete_previous_message_buttons
async def handle_answer(callback_query: types.CallbackQuery):
    user_id: int = callback_query.from_user.id
    msg = await QuizApp.finish_quiz(user_id)
    await callback_query.message.answer(msg)
   

async def main():
    await QuizApp.awake()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())