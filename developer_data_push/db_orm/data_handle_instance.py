#coding=utf-8

import __builtin__
import sys
import time
import pandas
from sqlalchemy import *
from db_instance import *

reload(sys)
sys.setdefaultencoding('utf8')


class pandas_instance(mysql_DB_instance):
    def __init__(self, dbUserName, dbPasswd, dbAddress, dbPort=3306, dbName=None, charset='utf8',
                    *args, **kwarg):
        super(pandas_instance, self).__init__(dbUserName,dbPasswd,dbAddress,dbPort,dbName,charset)

    def create_dataframe(self, name, SQLstatement):
        if not hasattr(self, name):
            setattr(self, name, pandas.read_sql(SQLstatement,self.conn))

    def get_dataframe(self, name):
        if hasattr(self, name):
            return getattr(self, name)

    def delete_dateframe(self,name):
        if hasattr(self, name):
            delattr(self, name)

    def create_task_district_groupby_unitshape(self, df):
        for casetime in df['CaseTime'].value_counts().keys():
            for districtname in df['DistrictName'].value_counts().keys():
                for housetype in df['HouseType'].value_counts().keys():
                    sub_df = df[(df['CaseTime']==casetime)&\
                            (df['DistrictName']==districtname)&\
                            (df['HouseType']==housetype)]
                    if sub_df.empty:
                        pass
                    else:
                        for key in sub_df['UnitShape'].value_counts().keys():
                            pass
        

    def create_task_district_groupby_area(self, df):
        pass

    def create_task_district_groupby_totalprice(self, df):
        pass
    
    def create_task_district_groupby_unitprice(self, df):
        pass

    def create_task_zone_groupby_unitshape(self, df):
        pass

    def create_task_zone_groupby_area(self, df):
        pass

    def create_task_zone_groupby_totalprice(self, df):
        pass

    def create_task_zone_groupby_unitprice(self, df):
        pass

    def create_task_residentialarea_groupby_unitshape(self, df):
        pass

    def create_task_residentialarea_groupby_area(self, df):
        pass

    def create_task_residentialarea_groupby_totalprice(self, df):
        pass

    def create_task_residentialarea_groupby_unitprice(self, df):
        pass
    