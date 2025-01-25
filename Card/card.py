from random import shuffle

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