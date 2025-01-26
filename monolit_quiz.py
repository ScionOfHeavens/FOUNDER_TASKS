from random import randint
from User.userDB import UserDB
from Card.deck import Deck

udb = UserDB()
deck = Deck()

class UI:
    def greet():
        print("Добро пожаловать")
    
    def ask_question(question: str) -> None:
        print("Следующий вопрос")
        print(question)

    def __prepare_options(options: list[str]) -> dict[str,str]:
        return dict(zip("abcdefgh", options))

    def suggest_answers(options: list[str]) -> None:
        print("Варианты ответов:")
        prepared_options: dict = UI.__prepare_options(options)
        for letter, option in prepared_options.items():
            print(f"{letter}) {option}")
    
    def get_answer(options: list[str]) -> str:
        prepared_options: dict = UI.__prepare_options(options)
        has_got_answer = False
        while not has_got_answer:
            answer = input()
            if answer in prepared_options:
                answer = prepared_options[answer]
            if answer in prepared_options.values():
                return answer
            print("Вы ввели невозможный ответ. Повторите снова")

class QuizApp:
    def start_main_loop() -> None:
        user_id = randint(1,1000)
        user = udb.get_user(user_id)
        while True:
            UI.greet()
            card = deck.get_card(user.question_id)
            
            UI.ask_question(card.question)
            options = card.options
            UI.suggest_answers(options)
            answer: str = UI.get_answer(options)    

            if card.is_true_option(answer):
                print("Это верный ответ!")
            else:
                print("Это не верно")

            if deck.is_finish_card(card):
                print("Поздравляем, вы ответили на все вопросы! Начнем заново!")
                udb.update_quiz_index(user.id, 1)
            else:
                udb.update_quiz_index(user.id, card.id + 1)

QuizApp.start_main_loop()