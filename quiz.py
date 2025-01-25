from random import shuffle, randint

class Card:
    __index: int
    __question: str
    __false_options: list[str]
    __true_option: str

    def __init__(self, index: int,  d: dict):
        self.__false_options = d["false_options"]
        self.__true_option = d["true_option"]
        self.__question = d["question"]
        self.__index = index

    @property
    def id(self):
        return self.__index
    @property
    def question(self)->str:
        return self.__question
    @property
    def false_options(self) -> list[str]:
        return self.__false_options.copy()  
    @property
    def true_option(self) -> str:
        return self.__true_option
    @property
    def options(self) -> list[str]:
        options = self.false_options + [self.true_option]
        shuffle(options)
        return options

    def is_true_option(self, option:str) -> bool:
        return self.__true_option == option


class Deck:
    __cards: dict[int, Card]
    def __init__(self):
        db = [
            {
                'question': 'Что такое Python?',
                'false_options': ['Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
                'true_option': 'Язык программирования'
            },
            {
                'question': 'Какой тип данных используется для хранения целых чисел?',
                'false_options': ['float', 'str', 'natural'],
                'true_option': 'int'
            },
        ]
        self.__cards = {i: Card(i,e) for i,e in zip(range(1, len(db)+1), db)}

    def get_card(self, index: int) -> Card:
        return self.__cards[index]
    def is_finish_card(self, card: Card) -> bool:
        return card.id == len(self.__cards)


class User:
    __id: int
    __quistion_id: int
    def __init__(self, id: int, question: int) -> None:
        self.__id = id
        self.__question_id = question
    @property
    def id(self):
        return self.__id
    @property
    def question_id(self) -> None:
        return self.__question_id


class UserDB:
    __users: dict[int, str]
    def __init__(self) -> None:
        self.__users = {}

    def get_user(self, user_id: int) -> User:
        if user_id not in self.__users:
            self.add_user(user_id)
        return self.__users[user_id]
        
    def add_user(self, user_id: int):
        self.__users[user_id] = (User(user_id, 1))

    def update_quiz_index(self, user_id: int, question_index: int) -> None:
        if not user_id in self.__users:
            self.add_user(user_id)
        self.__users[user_id] = User(user_id, question_index)

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
        while True:
            UI.greet()
            user = udb.get_user(user_id)
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