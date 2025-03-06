from User.user import User
from Services.SQLiteDataBase import SQLiteDataBase, SQLiteTable
from Services.YandexDataBase import YandexDataBase

class UserDB:
    async def awake(self) -> None:
        pass
    async def get_user(self, user_id: int) -> User:
        pass
    async def add_user(self, user: User) -> None:
        pass
    async def update_user(self, user: User) -> None:
        pass
    async def get_all_users(self) -> list[User]:
        pass


class UserSQLiteDB(UserDB):
    __users: SQLiteTable
    async def awake(self):
        db = SQLiteDataBase("users.db", r".\User")
        self.__users = await db.create_cls_table("users", User)
    
    async def add_user(self, user: User) -> None:
        await self.__users.create_record(user)
    
    async def get_user(self, user_id: int) -> User:
        user = await self.__users.read_record(user_id)
        if user == None:
            user = User(user_id)
            self.add_user(user)
        return user
    
    async def update_user(self, user: User) -> None:
        await self.__users.update_record(user)
    
    async def get_all_users(self) -> list[User]:
        return await self.__users.read_all_records()


class UserYDB(UserDB):
    __users: SQLiteTable
    async def awake(self):
        db = YandexDataBase()
        self.__users = await db.create_cls_table("users", User)
    
    async def add_user(self, user: User) -> None:
        await self.__users.create_record(user)
    
    async def get_user(self, user_id: int) -> User:
        user = await self.__users.read_record(user_id)
        if user == None:
            user = User(user_id)
            self.add_user(user)
        return user
    
    async def update_user(self, user: User) -> None:
        await self.__users.update_record(user)
    
    async def get_all_users(self) -> list[User]:
        return await self.__users.read_all_records()