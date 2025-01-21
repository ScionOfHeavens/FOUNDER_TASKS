class Card:
    __question: str
    __answer_options: list[str]

    def __init__(self, d: list[str]):
        self.__answer_options = d["options"]
        self.__question = d["q"]

    @property
    def question(self)->str:
        return self.__question
    @property
    def answer_options(self)->list[str]:
        return self.__answer_options.copy()

    def is_true_option(self, option:str) -> bool:
        return self.answer_options[0] == option

class Quiz:
    cards: list[Card]
    