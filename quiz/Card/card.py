from dataclasses import dataclass
from random import shuffle

@dataclass
class Card:
    __id: int
    __question: str
    __false_options: list[str]
    __true_option: str

    def __init__(self, id: int = 0, false_options: list[str] = [], true_option: str = "", question: str = ""):
        self.__false_options = false_options
        self.__true_option = true_option
        self.__question = question
        self.__id = id

    @property
    def id(self):
        return self.__id
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
    
    def serialize(self) -> dict:
        return {v.removeprefix('_' + self.__class__.__name__ + '__'):self.__getattribute__(v) for v in self.__dict__}