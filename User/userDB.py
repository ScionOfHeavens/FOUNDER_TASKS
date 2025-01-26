from User.user import User

class UserDB:
    __users: dict[int, str]
    def __init__(self) -> None:
        self.__users = {}

    async def get_user(self, user_id: int) -> User:
        if user_id not in self.__users:
            await self.add_user(user_id)
        return self.__users[user_id]
        
    async def add_user(self, user_id: int):
        self.__users[user_id] = (User(user_id, 1))

    async def update_quiz_index(self, user_id: int, question_index: int) -> None:
        if not user_id in self.__users:
            await self.add_user(user_id)
        self.__users[user_id] = User(user_id, question_index)