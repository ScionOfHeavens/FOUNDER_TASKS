from random import shuffle

class Card:
    __question: str
    __false_options: list[str]
    __true_option: str

    def __init__(self, d: list[str]):
        self.__false_options = d["false_options"]
        self.__true_option = d["true_option"]
        self.__question = d["question"]

    @property
    def question(self)->str:
        return self.__question
    @property
    def false_option(self) -> list[str]:
        return self.__false_options.copy()
    
    @property
    def true_option(self) -> str:
        return self.__true_option

    def is_true_option(self, option:str) -> bool:
        return self.__true_option == option


class Deck:
    __cards: list[Card]
    def __init__(self):
        self.__cards = []

    def get_card(self, index: int) -> Card:
        return self.cards[index]


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
    __users: list[User]
    def __init__(self) -> None:
        self.__users = []
    def get_quiz_index(self, user_index: int) -> None:
        return self.__users[user_index]
    def increment_quiz_index(self, user_index: int) -> None:
        question_id = self.__users[user_index].question_id
        self.__users[user_index] = User(user_index, question_id + 1)
    def update_quiz_index(self, user_index: int, question_index: int) -> None:
        self.__users[user_index] = User(user_index, question_index)


class UI:
    def start_quiz() -> None:
        print("Добро пожаловать в Quiz")
    
    def print_card(self, question_number, question, options) -> None:
        print(f"Вопрос номер {question_number}:")
        print(question)
        # self.__options = self.__current_card.__false_options + [self.__current_card.true_option]
        # shuffle(self.__options)
        print("Варианты ответов:")
        for number, option in dict(zip(range(1,16),options)):
            print(f"{number}) {option}")

    def take_answere(self, options: dict) -> str:
        answere = input()
        if answere in options.keys():
            return options[answere]
        if answere in options.values():
            return answere
        print("Enter valid answere, please.")
        return self.take_answere()


class QuizApp:
    __deck: Deck = Deck()
    __userDB: UserDB = UserDB()