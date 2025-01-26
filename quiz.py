from User.userDB import UserDB, UserDictDB, UserSQLiteDB
from Card.card import Card
from Card.deck import Deck

class QuizApp:
    __user_db: UserDB = UserSQLiteDB()
    __deck: Deck = Deck()
    async def awake():
        await QuizApp.__user_db.awake()

    async def prepare_next_question(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        next_question_id: int
        if await QuizApp.is_final_question(user_id):
            next_question_id = 1
        else:
            next_question_id = user.question_id + 1
        await QuizApp.__user_db.update_quiz_index(user_id, next_question_id)

    async def get_question(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return card.question
    
    async def get_options(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return card.options
    
    async def is_true_answer(user_id: int, answer: str):
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return card.is_true_option(answer)
    
    async def get_true_option(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return card.true_option
    
    async def is_final_question(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        card = await QuizApp.__deck.get_card(user.question_id)
        return await QuizApp.__deck.is_finish_card(card)
    
    async def restart_quiz(user_id: int):
        user = await QuizApp.__user_db.update_quiz_index(user_id, 1)