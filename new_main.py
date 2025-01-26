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

def generate_options_keyboard(options):
    builder = InlineKeyboardBuilder()
    for option in options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"user answer is {option}")
        )
    builder.adjust(1)
    return builder.as_markup()

@dp.callback_query(F.data.contains("user answer"))
async def check_answer(callback_query: types.CallbackQuery):
    answer = callback_query.data.removeprefix("user answer is ")
    user_id = callback_query.from_user.id
    if await QuizApp.is_true_answer(user_id, answer):
        await callback_query.message.answer("Верно!")
    else:
        await callback_query.message.answer("Неверно!")
        true_answer = await QuizApp.get_true_option(user_id)
        await callback_query.message.answer(f"Неправильно. Правильный ответ: {true_answer}")
    if not await QuizApp.is_final_question(user_id):
        await QuizApp.prepare_next_question(user_id)
        await play_card(callback_query.message, user_id)
    else:
        await callback_query.message.answer("Это был последний вопрос. Квиз завершен!")
        await QuizApp.restart_quiz(user_id)

async def play_card(message: types.Message, user_id: int):
    question = await QuizApp.get_question(user_id)
    options = await QuizApp.get_options(user_id)
    keyboard = generate_options_keyboard(options)
    await message.answer(question, reply_markup=keyboard)

@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def start_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!\nВопрос:")
    await play_card(message, message.from_user.id)


@dp.message(Command("start"))
async def start_cmd_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру")) 
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def main():
    await QuizApp.awake()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())