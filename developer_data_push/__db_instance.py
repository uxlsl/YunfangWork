#coding=utf-8

import __builtin__
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


class mssql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=1433, dbName=None, charset='utf8',
                    *args, **kwarg):
        self.__mssql_format = "mssql+pymssql://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/{dbName}?charset={charset}"
        self.__mssql_path = self.__mssql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort, dbName=dbName, charset=charset)
        self.engine = create_engine(self.__mssql_path, echo=False)
        self.metadata = MetaData(self.engine)
        self.__Base = declarative_base(metadata=self.metadata)
        self.__Base.metadata.reflect(self.engine)
        for table_name in self.__Base.metadata.tables:
            setattr(self,
                    table_name, __builtin__.type(str(table_name),
                                                    (self.__Base,),
                                                        {'__table__':self.__Base.metadata.tables[table_name]}))


class mysql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=3306, dbName=None, charset='utf8',
                    *args, **kwarg):
        self.__mysql_format = "mysql+pymysql://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/{dbName}?charset={charset}"
        self.__mysql_path = self.__mysql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort, dbName=dbName, charset=charset)
        self.engine = create_engine(self.__mysql_path, echo=False)
        self.metadata = MetaData(self.engine)
        self.__Base = declarative_base(metadata=self.metadata)
        self.__Base.metadata.reflect(self.engine)
        for table_name in self.__Base.metadata.tables:
            setattr(self,
                    table_name, __builtin__.type(str(table_name),
                                                    (self.__Base,),
                                                        {'__table__':self.__Base.metadata.tables[table_name]}))

    def create_schema(self,):
        pass

    def drop_schema(self,):
        pass

    def query_schema(self,):
        pass
