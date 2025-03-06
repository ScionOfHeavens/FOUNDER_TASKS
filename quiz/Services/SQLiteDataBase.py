import aiosqlite

class SQLiteTable:
    __table_name: str
    __data_base_name: str
    __cls: type
    def __init__(self, table_name: str, data_base_name: str, cls: type):
        self.__table_name = table_name
        self.__data_base_name = data_base_name
        self.__cls = cls
    
    def serialize_obj_attributes(self, obj: object):
        attributes = {}
        for attr_name_with_prefix in obj.__dict__:
            attr_name = attr_name_with_prefix.removeprefix('_' + obj.__class__.__name__ + '__')
            attributes[attr_name] = obj.__getattribute__(attr_name_with_prefix)
        return attributes

    async def create_record(self, obj: object) -> None:
        serialized_object = self.serialize_obj_attributes(obj)
        async with aiosqlite.connect(self.__data_base_name) as db:
            # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
            await db.execute(f'INSERT OR REPLACE INTO {self.__table_name} ({", ".join(serialized_object.keys())}) VALUES ({", ".join([str(e) for e in serialized_object.values()])})')
            # Сохраняем изменения
            await db.commit()
    
    async def read_record(self, id: int) -> object:
        results: tuple
        async with aiosqlite.connect(self.__data_base_name) as db:
            async with db.execute(f'SELECT * FROM {self.__table_name} WHERE id = {id}') as cursor:
                results = await cursor.fetchone()
        if results is not None:
            return self.__cls(*results)
        else:
            return None
        
    async def update_record(self, obj: object) -> None:
        await self.create_record(obj)

    async def read_all_records(self) -> list[object]:
        results: tuple
        async with aiosqlite.connect(self.__data_base_name) as db:
            async with db.execute(f'SELECT * FROM {self.__table_name}') as cursor:
                results = await cursor.fetchall()
        if results is not None:
            objs = []
            for result in results:
                objs.append(self.__cls(*result))
            return objs
        else:
            return None
    
    @property
    def name(self) -> str:
        return self.__table_name

    @property
    def database_name(self) -> str:
        return self.database_name
    

class SQLiteDataBase:
    __data_base_name: str
    __tables: list[SQLiteTable] = []
    def __init__(self, data_base_name:str, path:str="."):
        self.__data_base_name = path + '\\' + data_base_name

    def serialize_cls_attributes(self, cls: type):
        attributes = {}
        for atrr_name in cls.__annotations__:
            atrr_name = atrr_name.removeprefix('_' + cls.__name__ + '__')
            attributes[atrr_name] = "INTEGER"
        return attributes

    async def create_cls_table(self, table_name: str, cls: type) -> SQLiteTable:
        column_names = self.serialize_cls_attributes(cls)
        insert_parameters = ", ".join([k+" "+ v for k, v in column_names.items() if k != 'id'])
        async with aiosqlite.connect(self.__data_base_name) as db:
            await db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {insert_parameters})")
            await db.commit()
        self.__tables.append(SQLiteTable(table_name, self.__data_base_name, cls))
        return self.__tables[-1]
    
    async def execute(self, query: str) -> None:
        async with aiosqlite.connect(self.__data_base_name) as db:
            await db.execute(query)
            await db.commit()

    @property
    def tables(self) -> list[SQLiteTable]:
        return self.__tables.copy()
    
    def name(self) -> str:
        return self.__data_base_name