from User.user import User
from Services.SQLiteDataBase import SQLiteDataBase, SQLiteTable

class UserDB:
    async def awake(self) -> None:
        pass
    async def get_user(self, user_id: int) -> User:
        pass
    async def add_user(self, user: User) -> None:
        pass
    async def update_user(self, user: User) -> None:
        pass

# class UserSQLiteDB(UserDB):
#     __DB_NAME = r"User/users.db"
#     async def awake(self):
#         async with aiosqlite.connect(self.__DB_NAME) as db:
#             # Создаем таблицу
#             await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
#             # Сохраняем изменения
#             await db.commit()

#     async def get_user(self, user_id: int) -> User:
#         results: int
#         async with aiosqlite.connect(self.__DB_NAME) as db:
#             async with db.execute(f'SELECT * FROM  WHERE user_id = {user_id}') as cursor:
#                 results = await cursor.fetchone()
#         if results is not None:
#             return User(*results)
#         else:
#             await self.add_user(user_id)
#             return await self.get_user(user_id)
        
#     async def add_user(self, user: User) -> None:
#         serialized_user = user.serialize()
#         async with aiosqlite.connect(self.__DB_NAME) as db:
#             # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
#             await db.execute('INSERT INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, 1))
#             # Сохраняем изменения
#             await db.commit()

#     async def update_quiz_index(self, user_id: int, question_index: int) -> None:
#         async with aiosqlite.connect(self.__DB_NAME) as db:
#             # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
#             await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, question_index))
#             # Сохраняем изменения
#             await db.commit()

class UserSQLiteDB(UserDB):
    __users: SQLiteTable
    async def awake(self):
        db = SQLiteDataBase("users.db", r".\User")
        self.__users = await db.create_cls_table("users", User)
    
    async def add_user(self, user: User) -> None:
        await self.__users.create_record(user)
    
    async def get_user(self, user_id: int) -> User:
        return await self.__users.read_record(user_id)
    
    async def update_user(self, user: User) -> None:
        await self.__users.update_record(user)
    
    async def get_all_user(self) -> list[User]:
        return await self.__users.read_all_records()