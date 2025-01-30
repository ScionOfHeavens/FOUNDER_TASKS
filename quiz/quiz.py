from dataclasses import dataclass, asdict
import json
import ast
import sys

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from User.userDB import UserDB, UserSQLiteDB
from User.user import User
from Card.card import Card
from Card.deck import Deck

class QuizApp:
    __user_db: UserDB = UserSQLiteDB()
    __deck: Deck = Deck()
    async def awake():
        await QuizApp.__user_db.awake()

    async def get_card_user_from(user_id: int) -> tuple[Card, User]:
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return card, user

    async def check_answer(answer: str, user_id: int) -> str:
        answer = answer.removeprefix("Answer:")
        card, user = await QuizApp.get_card_user_from(user_id)
        user: User
        card: Card
        reply_msg = ""
        if card.is_true_option(answer):
            user = User.increment_current_result(user)
            await QuizApp.__user_db.update_user(user)
            reply_msg += "Ответ верный!\n"
        else:
            reply_msg += f"Ответ неверен!\n"
        for option in card.options:
            if option == answer:
                reply_msg += "✅ " if card.is_true_option(answer) else "❌ "
            else:
                reply_msg += "     "
            reply_msg += f"{option}\n"
        return reply_msg

    async def prepare_next_question(user_id:int = 0, to_continue:bool=False) -> tuple[str, str]:
        if user_id == 0:
            return "Получить первый вопрос", "QuestionQuery"
        card, user = await QuizApp.get_card_user_from(user_id)
        if to_continue:
            next_card = card
        else:
            next_card = await QuizApp.__deck.get_next(card)
        user = User.update_question(user, next_card.id)
        await QuizApp.__user_db.update_user(user)
        if await QuizApp.__deck.is_finish_card(card):
            return "Завершить Квиз", "FinishQuiz"
        return "Получить следующий вопрос", "QuestionQuery"

    async def play_card(user_id: int) -> tuple[str ,types.InlineKeyboardMarkup]:
        card, user = await QuizApp.get_card_user_from(user_id)
        question = card.question
        keyboard = QuizApp.__generate_options_keyboard(user, card)
        return question, keyboard

    async def start_quiz(user_id: int) -> None:
        user = await QuizApp.__user_db.get_user(user_id)
        user = User.update_question(user, 1)
        await QuizApp.__user_db.update_user(user)

    async def finish_quiz(user_id: int) -> str:
        user = await QuizApp.__user_db.get_user(user_id)
        current = user.current_result
        user = User.increment_current_tries(user)
        user = User.update_best(user)
        await QuizApp.__user_db.update_user(user)
        msg = "Спасибо за прохождение Квиза!\n"
        questions_amount = await QuizApp.__deck.questions_amount()
        user_info  = user.info
        msg += f"Ваш результат {current}/{questions_amount}\n"
        msg += f"Ваш лучший результат {user_info[0]}/{questions_amount}\n"
        msg += f"Вы прошли квиз {user_info[1]} раз(а)"
        return msg
    
    async def get_statistics() -> str:
        users = await QuizApp.__user_db.get_all_users()
        msg = "Общая статистика:\n"
        msg += "id                     current  best  tries\n"
        for user in users:
            best, tries, current = user.info
            msg += f"{user.id}        {current}         {best}         {tries}\n"
        return msg
    
    def __generate_options_keyboard(user:User,card: Card):
        builder = InlineKeyboardBuilder()
        for option in card.options:
            builder.add(
                types.InlineKeyboardButton(
                text=option,
                callback_data=f"Answer:{option}"
                )
            )
        builder.adjust(1)
        return builder.as_markup()