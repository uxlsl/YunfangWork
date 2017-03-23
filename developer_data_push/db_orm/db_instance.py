#coding=utf-8

# it need Sql server native client for linux #
# pymssql not support unicode #

import __builtin__
import sys
import db_mapper
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

reload(sys)
sys.setdefaultencoding('utf8')


class mssql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=1433, dbName=None, charset='utf8',
                    *args, **kwarg):
        self.tab_list = {}
        self.db_name = dbName
        self.__mssql_format = "mssql+pyodbc://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/{dbName}?driver=SQL+Server+Native+Client+11.0"
        self.__mssql_path = self.__mssql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort, dbName=dbName)
        self.engine = create_engine(self.__mssql_path, echo=False)
        self.conn = self.engine.connect()
        self.metadata = MetaData(self.engine)
        self.__Base = declarative_base(metadata=self.metadata)
        self.__Base.metadata.reflect(self.engine)
        for table_name in self.__Base.metadata.tables:
            print dbName,table_name
            try:
                setattr(self,
                        table_name, __builtin__.type(str(table_name),
                                                        (self.__Base,),
                                                            {'__table__':self.__Base.metadata.tables[table_name]}))
                self.tab_list[table_name] = (getattr(self,table_name))
            except Exception as e:
                print Exception,":",e
                if 'could not assemble any primary key' in e.message:
                    setattr(self,
                            table_name, __builtin__.type(str(table_name),
                                                            (self.__Base,),
                                                                {'__table__':self.__Base.metadata.tables[table_name],
                                                                '__mapper_args__':{'primary_key':[self.__Base.metadata.tables[table_name].c.Id,]}}))
                    self.tab_list[table_name] = (getattr(self,table_name))  
                print "add primary key id"    
        self.__Session = sessionmaker(bind=self.engine)
        self.__session = self.__Session()

    def create_schema(self, tableName, *args, **kwarg):
        try:
            cur_table = Table(tableName,
                                self.metadata,
                                Column('Tid',self.__type_map['int'],
                                        primary_key=True, autoincrement=True))
            for key in kwarg:
                cur_table.append_column(Column(key, self.__type_map[kwarg[key]]))
            cur_table.create()
            setattr(self,
                    tableName, 
                    __builtin__.type(str(tableName),
                                        (self.__Base,),
                                        {
                                            '__table__':cur_table
                                        }
                        ))
            self.tab_list[table_name] = (getattr(self,table_name))
        except Exception as e:
            print Exception,":",e
        finally:
            return
        
    def drop_schema(self, *args, **kwarg):
        # it will be finished in version 2 
        pass

    def query_schema(self, tableName, *args, **kwarg):
        table_object = getattr(self,tableName)
        result = None
        if "SQLstatement" in kwarg:
            if kwarg['SQLstatement']:
                SQLstatement = kwarg['SQLstatement']
                try:
                    result = self.__session.query(table_object).from_statement(SQLstatement).all()
                except Exception as e:
                    print Exception,":",e
                return result



class mysql_DB_instance(object):
    def __init__(self,
                    dbUserName, dbPasswd, dbAddress, dbPort=3306, dbName=None, charset='utf8',
                    *args, **kwarg):
        self.tab_list = {}
        self.db_name = dbName
        self.__type_map = db_mapper.type_map
        self.__mysql_format = "mysql+pymysql://{dbUserName}:{dbPasswd}@{dbAddress}:{dbPort}/{dbName}?charset={charset}"
        self.__mysql_path = self.__mysql_format.format(dbUserName=dbUserName, dbPasswd=dbPasswd, dbAddress=dbAddress,
                                                    dbPort=dbPort, dbName=dbName, charset=charset)
        self.engine = create_engine(self.__mysql_path, echo=False)
        self.conn = self.engine.connect()
        self.metadata = MetaData(self.engine)
        self.__Base = declarative_base(metadata=self.metadata)
        self.__Base.metadata.reflect(self.engine)
        for table_name in self.__Base.metadata.tables:
            print dbName,table_name
            try:
                setattr(self,
                        table_name, __builtin__.type(str(table_name),
                                                        (self.__Base,),
                                                            {'__table__':self.__Base.metadata.tables[table_name]}))
                self.tab_list[table_name] = (getattr(self,table_name))
            except Exception as e:
                print Exception,":",e
                if 'could not assemble any primary key' in e.message:
                    try:
                        setattr(self,
                                table_name, __builtin__.type(str(table_name),
                                                                (self.__Base,),
                                                                    {'__table__':self.__Base.metadata.tables[table_name],
                                                                    '__mapper_args__':{'primary_key':[self.__Base.metadata.tables[table_name].c.id,]}}))
                        self.tab_list[table_name] = (getattr(self,table_name))  
                        print "add primary key id"
                    except Exception as e:
                        print Exception,":",e 
        self.__Session = sessionmaker(bind=self.engine)
        self.__session = self.__Session()

    def create_schema(self, tableName, *args, **kwarg):
        try:
            cur_table = Table(tableName,
                                self.metadata,
                                Column('Tid',self.__type_map['int'],
                                        primary_key=True, autoincrement=True))
            for key in kwarg:
                cur_table.append_column(Column(key, self.__type_map[kwarg[key]]))
            cur_table.create()
            setattr(self,
                    tableName, 
                    __builtin__.type(str(tableName),
                                        (self.__Base,),
                                        {
                                            '__table__':cur_table
                                        }
                        ))
            self.tab_list[table_name] = (getattr(self,table_name))
        except Exception as e:
            print Exception,":",e
        finally:
            return
        
    def drop_schema(self, *args, **kwarg):
        # it will be finished in version 2 
        pass

    def query_schema(self, tableName, *args, **kwarg):
        table_object = getattr(self,tableName)
        result = None
        if "SQLstatement" in kwarg:
            if kwarg['SQLstatement']:
                SQLstatement = kwarg['SQLstatement']
                try:
                    result = self.__session.query(table_object).from_statement(SQLstatement).all()
                except Exception as e:
                    print Exception,":",e
                return result

