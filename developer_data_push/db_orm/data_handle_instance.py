#coding=utf-8

import __builtin__
import sys
import time
import pandas
from sqlalchemy import *
from db_instance import *

reload(sys)
sys.setdefaultencoding('utf8')

tableNameList = [
    'district_groupby_unitshape',
    'district_groupby_area',
    'district_groupby_totalprice',
    'district_groupby_unitprice',
    'zone_groupby_unitshape',
    'zone_groupby_area',
    'zone_groupby_totalprice',
    'zone_groupby_unitprice',
    'resdentialarea_groupby_unitshape',
    'resdentialarea_groupby_area',
    'resdentialarea_groupby_totalprice',
    'resdentialarea_groupby_unitprice',
]

area_lower = 20
area_upper = 140
area_step = 5
area_begin_num = area_lower
unitprice_lower = 3000
unitprice_upper = 100000
unitprice_step = 1000
unitprice_begin_num = unitprice_lower
totalprice_lower = 300000
totalprice_upper = 9999999
totalprice_step = 100000
totalprice_begin_num = totalprice_lower

area_sections = [('min_area',area_lower),(area_upper,'max_area'),]
unitprice_sections = [('min_unitprice',unitprice_lower),(unitprice_upper,'max_unitprice'),]
totalprice_sections = [('min_totalprice',totalprice_lower),(totalprice_upper,'max_totalprice'),]

while True:
    if area_begin_num+area_step >= area_upper:
        add_tuple = (area_begin_num,area_upper)
        area_sections.append(add_tuple)
        area_begin_num = area_lower
        break
    else:
        add_tuple = (area_begin_num,area_begin_num+area_step)
        area_sections.append(add_tuple)
        area_begin_num += area_step

while True:
    if unitprice_begin_num+unitprice_step >= unitprice_upper:
        add_tuple = (unitprice_begin_num,unitprice_upper)
        unitprice_sections.append(add_tuple)
        unitprice_begin_num = unitprice_lower
        break
    else:
        add_tuple = (unitprice_begin_num,unitprice_begin_num+unitprice_step)
        unitprice_sections.append(add_tuple)
        unitprice_begin_num += unitprice_step

while True:
    if totalprice_begin_num+totalprice_step >= totalprice_upper:
        add_tuple = (totalprice_begin_num,totalprice_upper)
        totalprice_sections.append(add_tuple)
        totalprice_begin_num = totalprice_lower
        break
    else:
        add_tuple = (totalprice_begin_num,totalprice_begin_num+totalprice_step)
        totalprice_sections.append(add_tuple)
        totalprice_begin_num += totalprice_step



def update_to_database(connection, tableName, updateValue, **kwarg):
    if (not connection) or (not tableName):
        print "get no connection or table to process"
        return
    else:
        select_sql = 'select * from {tableName} where 1=1'.format(tableName=tableName)
        for key in kwarg:
            select_sql += ' and {keyName} = {keyValue}'.format(keyName=key,keyValue=kwarg[key])
        res = connection.execute(select_sql+' for update').first()
        if res:
            update_sql = 'update {tableName} set ZaiShouTaoShu = {updateValue} where 1=1'.\
                            format(tableName=tableName,updateValue=updateValue)
            for key in kwarg:
                update_sql += ' and {keyName} = {keyValue}'.format(keyName=key,keyValue=kwarg[key])
            connection.execute(update_sql)
        else:
            key_list = []
            value_list = []
            for key in kwarg:
                key_list.append(key)
                value_list.append(kwarg[key])
            key_list.append('XinZengGongYingTaoShu')
            value_list.append(updateValue)
            key_list_str = '('+','.join(key_list)+')'
            value_list_str = '('+','.join(value_list)+')'
            insert_sql = 'insert into {tableName} {key_list} values {value_list}'.\
                            format(tableName=tableName,key_list=key_list_str,value_list=value_list_str)
            connection.execute(insert_sql)





class pandas_instance(mysql_DB_instance):
    def __init__(self, dbUserName, dbPasswd, dbAddress, dbPort=3306, dbName=None, charset='utf8',
                    *args, **kwarg):
        super(pandas_instance, self).__init__(dbUserName,dbPasswd,dbAddress,dbPort,dbName,charset)
        self.distance_db_mysql = mysql_DB_instance(dbUserName='root', 
                                    dbPasswd='', 
                                    dbAddress='192.168.6.8', 
                                    dbName='develop_data')

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
                        print "Empty set"
                    else:
                        for key in sub_df['UnitShape'].value_counts().keys():
                            update_value = sub_df['UnitShape'].value_counts()[key]
                            update_to_database(connection=self.distance_db_mysql.conn, 
                                    tableName='district_groupby_unitshape', 
                                    updateValue="'%s'"%update_value,
                                    Chengshi="'北京'",
                                    XingZhengQu="'%s'"%districtname,
                                    HuXing="'%s'"%key,
                                    ShiJian="'%s'"%casetime,
                                    YeTai="'%s'"%housetype)
        
    def create_task_new(self, df):
        done_num = 0
        df = df.fillna('null')
        for buildingcompletedyear in df['BuildingCompletedYear'].value_counts().keys():
            sub_df_buildingcompletedyear = df[(df['BuildingCompletedYear']==buildingcompletedyear)]
            if sub_df_buildingcompletedyear.empty:
                continue
            for zone in sub_df_buildingcompletedyear['ZoneCaseFrom'].value_counts().keys():
                sub_df_zone = sub_df_buildingcompletedyear[(sub_df_buildingcompletedyear['ZoneCaseFrom']==zone)]
                if sub_df_zone.empty:
                    continue
                for residentialarea in sub_df_zone['ResidentialAreaName'].value_counts().keys():
                    sub_df_residentialarea = sub_df_zone[(sub_df_zone['ResidentialAreaName']==residentialarea)]
                    if sub_df_residentialarea.empty:
                        continue
                    for casetime in sub_df_residentialarea['CaseTime'].value_counts().keys():
                        sub_df_casetime = sub_df_residentialarea[(sub_df_residentialarea['CaseTime']==casetime)]
                        if sub_df_casetime.empty:
                            continue
                        for districtname in sub_df_casetime['DistrictName'].value_counts().keys():
                            sub_df_districtname = sub_df_casetime[(sub_df_casetime['DistrictName']==districtname)]
                            if sub_df_districtname.empty:
                                continue
                            for housetype in sub_df_districtname['HouseType'].value_counts().keys():
                                sub_df_housetype = sub_df_districtname[(sub_df_districtname['HouseType']==housetype)]
                                if sub_df_housetype.empty:
                                    continue
                                for unitshape in sub_df_housetype['UnitShape'].value_counts().keys():
                                    sub_df_unitshape = sub_df_housetype[(sub_df_housetype['UnitShape']==unitshape)]
                                    if sub_df_unitshape.empty:
                                        continue
                                    
                                    area_sections_tmp = list(area_sections)
                                    area_sections_done = []
                                    print sub_df_unitshape['BuildingArea'].max(), sub_df_unitshape['BuildingArea'].min()
                                    for section in area_sections_tmp:
                                        if not ((isinstance(section[0],int) and isinstance(section[1],int)) and \
                                            ((section[0]>sub_df_unitshape['BuildingArea'].max()) or (section[1]<sub_df_unitshape['BuildingArea'].min()))):
                                            #print "drop section: %s,%s"%section
                                            area_sections_done.append(section)
                                    for area_section in area_sections_done:
                                        area_section = list(area_section)
                                        area_section_str = "{low}~{up}".format(low=area_section[0],up=area_section[1])
                                        for index_bound,bound in enumerate(area_section):
                                            if isinstance(bound,str):
                                                if 'min' in bound:
                                                    area_section[index_bound] = 0
                                                if 'max' in bound:
                                                    area_section[index_bound] = 9999999999999
                                        area_lower_bound = area_section[0]
                                        area_upper_bound = area_section[1]
                                        sub_df_area = sub_df_unitshape[(sub_df_unitshape['BuildingArea']>=float(area_lower_bound))&(sub_df_unitshape['BuildingArea']<float(area_upper_bound))]
                                        if sub_df_area.empty:
                                            continue
                                        #print sub_df_area['Tid'].count()
                                       
                                        totalprice_sections_tmp = list(totalprice_sections)
                                        totalprice_sections_done = []
                                        print sub_df_area['TotalPrice'].max(), sub_df_area['TotalPrice'].min()
                                        for section in totalprice_sections_tmp:
                                            if not ((isinstance(section[0],int) and isinstance(section[1],int)) and \
                                                ((section[0]>sub_df_area['TotalPrice'].max()) or (section[1]<sub_df_area['TotalPrice'].min()))):
                                                #print "drop section: %s,%s"%section
                                                totalprice_sections_done.append(section)
                                        for totalprice_section in totalprice_sections_done:
                                            totalprice_section = list(totalprice_section)
                                            totalprice_section_str = "{low}~{up}".format(low=totalprice_section[0],up=totalprice_section[1])
                                            for index_bound,bound in enumerate(totalprice_section):
                                                if isinstance(bound,str):
                                                    if 'min' in bound:
                                                        totalprice_section[index_bound] = 0
                                                    if 'max' in bound:
                                                        totalprice_section[index_bound] = 9999999999999
                                            totalprice_lower_bound = totalprice_section[0]
                                            totalprice_upper_bound = totalprice_section[1]
                                            sub_df_totalprice = sub_df_area[(sub_df_area['TotalPrice']>=float(totalprice_lower_bound))&(sub_df_area['TotalPrice']<float(totalprice_upper_bound))]
                                            if sub_df_totalprice.empty:
                                                continue
                                            #print sub_df_totalprice
                                            
                                            unitprice_sections_tmp = list(unitprice_sections)
                                            unitprice_sections_done = []
                                            print sub_df_totalprice['UnitPrice'].max(), sub_df_totalprice['UnitPrice'].min()
                                            for section in unitprice_sections_tmp:
                                                if not((isinstance(section[0],int) and isinstance(section[1],int)) and \
                                                    ((section[0]>sub_df_totalprice['UnitPrice'].max()) or (section[1]<sub_df_totalprice['UnitPrice'].min()))):
                                                    #print "drop section: %s,%s"%section
                                                    unitprice_sections_done.append(section)
                                            for unitprice_section in unitprice_sections_done:
                                                unitprice_section = list(unitprice_section)
                                                unitprice_section_str = "{low}~{up}".format(low=unitprice_section[0],up=unitprice_section[1])
                                                for index_bound,bound in enumerate(unitprice_section):
                                                    if isinstance(bound,str):
                                                        if 'min' in bound:
                                                            unitprice_section[index_bound] = 0
                                                        if 'max' in bound:
                                                            unitprice_section[index_bound] = 9999999999999
                                                unitprice_lower_bound = unitprice_section[0]
                                                unitprice_upper_bound = unitprice_section[1]

                                                sub_df_done = sub_df_totalprice[(sub_df_totalprice['UnitPrice']>=float(unitprice_lower_bound))&\
                                                                        (sub_df_totalprice['UnitPrice']<float(unitprice_upper_bound))]
                                                if sub_df_done.empty:
                                                    print casetime,"北京",districtname,zone,buildingcompletedyear,\
                                                            residentialarea,housetype,unitshape,area_section_str,totalprice_section_str,\
                                                            unitprice_section_str
                                                    print "Empty set"
                                                else:
                                                    update_value = sub_df_done['Tid'].count()
                                                    sum_area = sub_df_done['BuildingArea'].sum()
                                                    print casetime,"北京",districtname,zone,buildingcompletedyear,\
                                                            residentialarea,housetype,unitshape,area_section_str,totalprice_section_str,\
                                                            unitprice_section_str
                                                    print update_value,sum_area
                                                    update_to_database(connection=self.distance_db_mysql.conn, 
                                                            tableName='district_groupby_area', 
                                                            updateValue="'%s'"%update_value,
                                                            Chengshi="'北京'",
                                                            XingZhengQu="'%s'"%districtname,
                                                            HuXing="'%s'"%unitshape,
                                                            ShiJian="'%s'"%casetime,
                                                            YeTai="'%s'"%housetype,
                                                            PianQu="'%s'"%zone,
                                                            XiaoQuMingCheng="'%s'"%residentialarea,
                                                            JianChengNianDai="'%s'"%buildingcompletedyear,
                                                            MianJiDuan="'%s'"%area_section_str,
                                                            ZongJiaDuan="'%s'"%totalprice_section_str,
                                                            DanJiaDuan="'%s'"%unitprice_section_str,
                                                            ZongMianJi="'%s'"%sum_area
                                                            )


    def create_task_exist(self, df):
        pass
    
    def create_task_district_groupby_unitprice(self, df):
        pass

    def create_task_zone_groupby_unitshape(self, df):
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

    def create_task_zone_groupby_area(self, df):
        pass

    def create_task_zone_groupby_totalprice(self, df):
        pass

    def create_task_zone_groupby_unitprice(self, df):
        pass

    def create_task_residentialarea_groupby_unitshape(self, df):
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

    def create_task_residentialarea_groupby_area(self, df):
        pass

    def create_task_residentialarea_groupby_totalprice(self, df):
        pass

    def create_task_residentialarea_groupby_unitprice(self, df):
        pass