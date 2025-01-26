from User.user import User
import aiosqlite

class UserDB:
    async def awake(self):
        pass
    async def get_user(self, user_id: int) -> User:
        pass
    async def add_user(self, user_id: int) -> None:
        pass
    async def update_quiz_index(self, user_id: int, question_index: int) -> None:
        pass

class UserDictDB(UserDB):
    __users: dict[int, str]
    async def awake(self):
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

class UserSQLiteDB(UserDB):
    __DB_NAME = r"User/users.db"
    async def awake(self):
        async with aiosqlite.connect(self.__DB_NAME) as db:
            # Создаем таблицу
            await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
            # Сохраняем изменения
            await db.commit()

    async def get_user(self, user_id: int) -> User:
        results: int
        async with aiosqlite.connect(self.__DB_NAME) as db:
            async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
                results = await cursor.fetchone()
        if results is not None:
            return User(user_id, results[0])
        else:
            await self.add_user(user_id)
            return await self.get_user(user_id)
        
    async def add_user(self, user_id: int) -> None:
        async with aiosqlite.connect(self.__DB_NAME) as db:
            # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
            await db.execute('INSERT INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, 1))
            # Сохраняем изменения
            await db.commit()

    async def update_quiz_index(self, user_id: int, question_index: int) -> None:
        async with aiosqlite.connect(self.__DB_NAME) as db:
            # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
            await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, question_index))
            # Сохраняем изменения
            await db.commit()