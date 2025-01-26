from User.userDB import UserDB
from Card.card import Card
from Card.deck import Deck

class QuizApp:
    __user_db: UserDB = UserDB()
    __deck: Deck = Deck()

    async def prepare_next_question(user_id: int):
        user = await QuizApp.__user_db.get_user(user_id)
        await QuizApp.__user_db.update_quiz_index(user_id, user.question_id + 1)

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