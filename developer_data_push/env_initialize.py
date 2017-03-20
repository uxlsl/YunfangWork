#coding=utf8

import sys
from db_orm.db_instance import mssql_DB_instance, mysql_DB_instance
reload(sys)
sys.setdefaultencoding('utf-8')


class main_ms_env(object):
    """docstring for ClassName"""
    def __init__(self):
        self.db_mysql_list = {}
        self.db_mssql_list = {}
        self.distance_db_mysql = mysql_DB_instance(dbUserName='root', 
                                    dbPasswd='', 
                                    dbAddress='192.168.6.8', 
                                    dbName='developer_data')
        self.db_mysql_list[self.distance_db_mysql.db_name] = self.distance_db_mysql

        self.source_db_mysql = mysql_DB_instance(dbUserName="root", 
                                            dbPasswd="gh001",  
                                            dbAddress="192.168.10.42", 
                                            dbName='casescore')
        self.db_mysql_list[self.source_db_mysql.db_name] = self.source_db_mysql
        self.find_all_available_db()
        self.configure_all_available_db()
        #self.initialize_data()

    def find_all_available_db(self):
        result = self.base_db_mssql.query_schema(tableName='TaskInfo',SQLstatement="select * from TaskInfo")
        if result and result != []:
            for row in result:
                db_name = row.DbName
                print db_name
                db_instance_id = row.AvailableDbInstanceId
                in_result = self.base_db_mssql.query_schema(tableName='AvailableDbInstance',
                                                            SQLstatement="select * \
                                                                from AvailableDbInstance \
                                                                where TID = {AvailableDbInstanceId}".\
                                                                format(AvailableDbInstanceId=db_instance_id))
                if in_result and in_result != []:
                    for in_row in in_result:
                        setattr(self, db_name, mssql_DB_instance(dbUserName=in_row.UserName,
                                                                dbPasswd=in_row.Password,
                                                                dbAddress=in_row.InstantceAddress,
                                                                dbName=db_name))
                        self.db_mssql_list[db_name] = getattr(self,db_name)

    def configure_all_available_db(self):
        for db in self.db_mssql_list:
            for table_name in self.db_mssql_list[db].metadata.tables.keys():
                print "Create table %s in mysql"%table_name
                table = self.db_mssql_list[db].metadata.tables[table_name]
                table.name = db+table_name
                table.metadata = self.db_mysql.metadata
                table.create()