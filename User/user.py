from dataclasses import dataclass
import json

@dataclass 
class User:
    __id: int
    __question_id: int
    __current_result: int
    __best_result: int
    __tries_amount: int
    def __init__(self, id: int, question: int = 1, current_result = 0, best_result:int = 0, tries_amount=0) -> None:
        self.__id = id
        self.__question_id = question
        self.__current_result = current_result
        self.__best_result = best_result
        self.__tries_amount = tries_amount
    @property
    def id(self): 
        return self.__id
    @property
    def question_id(self) -> None:
        return self.__question_id
    @property
    def info(self):
        return self.__best_result, self.__tries_amount, self.__current_result
    @property
    def current_result(self):
        return self.__current_result
    
    def increment_current_result(other):
        if isinstance(other, User):
            return User(other.__id, other.__question_id, other.__current_result+1, other.__best_result, other.__tries_amount)
        
    def increment_current_tries(other):
        if isinstance(other, User):
            return User(other.__id, other.__question_id, other.__current_result, other.__best_result, other.__tries_amount+1)
        
    def update_best(other):
        if isinstance(other, User):
            if other.__current_result > other.__best_result:
                return User(other.__id, other.__question_id, 0, other.__current_result, other.__tries_amount)
            else:
                return User(other.__id, other.__question_id, 0, other.__best_result, other.__tries_amount)
    
    def update_question(other, question_id: int):
        if isinstance(other, User):
            return User(other.__id, question_id, other.__current_result, other.__best_result, other.__tries_amount)


    def serialize(self) -> dict:
        return {v.removeprefix('_' + self.__class__.__name__ + '__'):self.__getattribute__(v) for v in self.__dict__}