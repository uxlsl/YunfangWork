#coding=utf8

import sys
from db_orm.db_instance_for_chinese import mssql_DB_instance, mysql_DB_instance
reload(sys)
sys.setdefaultencoding('utf-8')


class main_ms_env(object):
    """docstring for ClassName"""
    def __init__(self):
        self.db_mysql = mysql_DB_instance(dbUserName='root', 
                                    dbPasswd='', 
                                    dbAddress='192.168.6.8', 
                                    dbName='developer_data')
        self.base_db_mssql = mssql_DB_instance(dbUserName="sa", 
                                            dbPasswd="gh001",  
                                            dbAddress="192.168.14.76", 
                                            dbName='CheckData')
        self.find_all_available_db()
        self.configure_all_available_db()

    def find_all_available_db(self):
        result = self.base_db_mssql.query_schema(SQLstatement="select * from [{dbName}].[dbo].TaskInfo".\
                                                    format(dbName=self.base_db_mssql.db_name))
        if result and result != []:
            for row in result:
                print row
                db_name = row.DbName
                db_instance_id = row.AvailableDbInstanceId
                in_result = self.base_db_mssql.query_schema(SQLstatement="select * \
                                                                from [{dbName}].[dbo].AvailableDbInstance \
                                                                where TID = {AvailableDbInstanceId}".\
                                                                format(dbName=self.base_db_mssql.db_name,
                                                                    AvailableDbInstanceId=db_instance_id))
                if in_result and in_result != []:
                    for in_row in in_result:
                        setattr(self, db_name, mssql_DB_instance(dbUserName=in_row.UserName,
                                                                dbPasswd=in_row.Password,
                                                                dbAddress=in_row.InstantceAddress,
                                                                dbName=db_name))

    def configure_all_available_db(self):
        