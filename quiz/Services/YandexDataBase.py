import os
import ydb


class YDBTable:
    __table_name: str
    __data_base: object
    __cls: type
    def __init__(self, table_name: str, data_base: object, cls: type):
        self.__table_name = table_name
        self.__data_base = data_base
        self.__cls = cls

    def serialize_obj_attributes(self, obj: object):
        attributes = {}
        for attr_name_with_prefix in obj.__dict__:
            attr_name = attr_name_with_prefix.removeprefix('_' + obj.__class__.__name__ + '__')
            attributes[attr_name] = obj.__getattribute__(attr_name_with_prefix)
        return attributes

    async def create_record(self, obj: object) -> None:
        serialized_object = self.serialize_obj_attributes(obj)
        query = f"""
        UPSERT INTO `quiz_state` ({", ".join(serialized_object.keys())}) VALUES ({", ".join([str(e) for e in serialized_object.values()])});
        """
        self.__data_base.execute_update_query(query)
    
    async def read_record(self, id: int) -> object:
        results: tuple
        query = f"""
        SELECT * FROM `quiz_state`
        WHERE id == {id};
        """
        results = self.__data_base.execute_select_query(query)
        if len(results) != 0:
            return self.__cls(*(results[0]))
        else:
            return None
        
    async def update_record(self, obj: object) -> None:
        await self.create_record(obj)

    async def read_all_records(self) -> list[object]:
        results: tuple
        query = f"""
        SELECT * FROM `quiz_state`
        """
        results = self.__data_base.execute_select_query(query)
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

class YandexDataBase:
    YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
    YDB_DATABASE = os.getenv("YDB_DATABASE")
    pool: ydb.SessionPool
    _instance = None
    __tables: list[YDBTable] = []

    def __new__(cls) -> None:
        if cls.pool == None:
            cls.pool = cls.get_ydb_pool(cls.YDB_ENDPOINT, cls.YDB_DATABASE)
        if cls._instance == None:
            cls._instance = super(cls).__new__(cls)
            cls._instance.pool = cls.pool
        return cls._instance

    def get_ydb_pool(ydb_endpoint, ydb_database, timeout=30) -> ydb.SessionPool:
        ydb_driver_config = ydb.DriverConfig(
            ydb_endpoint,
            ydb_database,
            credentials=ydb.credentials_from_env_variables(),
            root_certificates=ydb.load_ydb_root_certificate(),
        )

        ydb_driver = ydb.Driver(ydb_driver_config)
        ydb_driver.wait(fail_fast=True, timeout=timeout)
        return ydb.SessionPool(ydb_driver)

    def _format_kwargs(kwargs):
        return {"${}".format(key): value for key, value in kwargs.items()}

    def execute_update_query(self, query, **kwargs):
        def callee(session: ydb.Session):
            prepared_query = session.prepare(query)
            session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, YandexDataBase._format_kwargs(kwargs), commit_tx=True
            )

        return self.pool.retry_operation_sync(callee)

    def execute_select_query(self, query, **kwargs):
        def callee(session: ydb.Session):
            prepared_query = session.prepare(query)
            result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, YandexDataBase._format_kwargs(kwargs), commit_tx=True
            )
            return result_sets[0].rows

        return self.pool.retry_operation_sync(callee)
    
    def serialize_cls_attributes(self, cls: type):
        attributes = {}
        for atrr_name in cls.__annotations__:
            atrr_name = atrr_name.removeprefix('_' + cls.__name__ + '__')
            attributes[atrr_name] = "Uint64"
        return attributes

    async def create_cls_table(self, table_name: str, cls: type) -> YDBTable:
        column_names = self.serialize_cls_attributes(cls)
        insert_parameters = ",\n".join([k+" "+ v for k, v in column_names.items() if k != 'id'])
        query = f'''CREATE TABLE {table_name} (
        id Uint64,
        {insert_parameters},
        PRIMARY KEY (`id`)
        );
        
        COMMIT;
        '''
        def callee(session: ydb.Session):
            prepared_query = session.prepare(query)
            session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, YandexDataBase._format_kwargs(), commit_tx=True
            )
        self.pool.retry_operation_sync(callee)
        self.__tables.append(YDBTable(table_name, self.__data_base_name, cls))
        return self.__tables[-1]

    @property
    def tables(self) -> list[YDBTable]:
        return self.__tables.copy()
    
    def name(self) -> str:
        return self.__data_base_name
