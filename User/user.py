from dataclasses import dataclass
import json

@dataclass 
class User:
    __id: int
    __question_id: int
    def __init__(self, id: int, question: int = 1) -> None:
        self.__id = id
        self.__question_id = question
    @property
    def id(self): 
        return self.__id
    @property
    def question_id(self) -> None:
        return self.__question_id
    
    def serialize(self) -> dict:
        return {v.removeprefix('_' + self.__class__.__name__ + '__'):self.__getattribute__(v) for v in self.__dict__}