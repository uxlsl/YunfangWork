#coding=utf-8

import __builtin__
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


class mssql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=1433, dbName=None,
                    *args, **kwarg):
        self.db_name = dbName
        self.__mssql_format = "mssql+pymssql://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/"
        self.__mssql_path = self.__mssql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort)
        self.engine = create_engine(self.__mssql_path, echo=False)
        self.__conn = self.engine.connect()
        self.__conn.execution_options(autocommit=True)

    def create_schema(self, tableName, *args, **kwarg):
        #it will be finished in version2
        pass
        
    def drop_schema(self, *args, **kwarg):
        # it will be finished in version 2 
        pass

    def query_schema(self, *args, **kwarg):
        res = None
        if "SQLstatement" in kwarg:
            if kwarg['SQLstatement']:
                SQLstatement = kwarg['SQLstatement']
                try:
                    result = self.__conn.execute(SQLstatement)
                    res = result.fetchall()
                except Exception as e:
                    print Exception,":",e
                finally:
                    return res



class mysql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=3306, dbName=None, charset='utf8',
                    *args, **kwarg):
        self.db_name = dbName
        self.__mysql_format = "mysql+pymysql://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/{dbName}?charset={charset}"
        self.__mysql_path = self.__mysql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort, dbName=dbName, charset=charset)
        self.engine = create_engine(self.__mysql_path, echo=False)
        self.__conn = self.engine.connect()
        self.__conn.execution_options(autocommit=True)

    def create_schema(self, tableName, *args, **kwarg):
        # it will be finished in version 2
        pass
        
    def drop_schema(self, *args, **kwarg):
        # it will be finished in version 2 
        pass

    def query_schema(self, tableName, *args, **kwarg):
        res = None
        if "SQLstatement" in kwarg:
            if kwarg['SQLstatement']:
                SQLstatement = kwarg['SQLstatement']
                try:
                    result = self.__conn.execute(SQLstatement)
                    res = result.fetchall()
                except Exception as e:
                    print Exception,":",e
                finally:
                    return res
