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