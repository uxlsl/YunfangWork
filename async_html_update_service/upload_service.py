#coding=utf-8

from __future__ import absolute_import

import sys
import os
import time
import paramiko
import sqlalchemy

from celery import Celery
from sqlalchemy import *
from sqlalchemy.orm import *
from async_html_update_service.celery import app

reload(sys)
sys.setdefaultencoding('utf-8')

db_user_name = "root"
db_passwd = ""
db_address = "192.168.6.8"
db_port = "3306"
db_name = "scrapy_data"
db_schema = "file_record_fdfs"

ssh_connect_pool = {}


def _get_Connect_from_Pool(ip,port,user,passwd):
    global ssh_connect_pool
    try:
        ssh_key = reduce(lambda x,y:x+":"+y,map(str, [ip,port,user,passwd]))
        if ssh_connect_pool.has_key(ssh_key):
            print "Success get an existing connection from pool."
            return ssh_connect_pool[ssh_key] 
        else:
            print "Create a new connection in pool."
            new_connection = paramiko.SSHClient()
            new_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            new_connection.connect(ip,port,user,passwd)
            ssh_connect_pool[ssh_key] = new_connection
            return new_connection
    except Exception as e:
        print Exception,":",e
        print "There is ERROR in getting ssh connection."


def _init():
    celery = Celery(broker="redis://192.168.6.4/2",backend="redis://192.168.6.4/3")
    try:
        _mysql_format = "mysql+pymysql://{db_user_name}:{db_passwd}@{db_address}:{db_port}/{db_name}?charset=utf8"
        _mysql_path = _mysql_format.format(db_user_name=db_user_name,
                                            db_passwd=db_passwd,
                                            db_address=db_address,
                                            db_port=db_port,
                                            db_name=db_name)
        engine = create_engine(_mysql_path,echo=False)
        metadata = MetaData(engine)
        try:
            file_record_fdfs = Table(db_schema,metadata,autoload=True)
            return file_record_fdfs,celery
        except Exception as e:
            print Exception,":",e
            if isinstance(e,sqlalchemy.exc.NoSuchTableError):
                print "Cannot find the table and create a new one."
                file_record_fdfs = Table(db_schema,metadata,
                                            Column('id',Integer,primary_key=True,autoincrement=True),
                                            Column('create_time',VARCHAR(30),nullable=False),
                                            Column('version_time',BigInteger,nullable=False),
                                            Column('source_route',VARCHAR(80),nullable=False),
                                            Column('file_name_full',VARCHAR(255),index=True,nullable=False),
                                            Column('file_source_path',VARCHAR(255),index=True,nullable=False),
                                            Column('file_name_shot',VARCHAR(255),index=True,nullable=False),
                                            Column('source_address',VARCHAR(20),index=True,nullable=False),
                                            Column('file_store_id',VARCHAR(255),index=True,nullable=False),
                                            mysql_engine="InnoDB",mysql_charset="utf8")
                file_record_fdfs.create()
                print "success."
                return file_record_fdfs,celery
            else:
                return
    except Exception as e:
        print Exception,":",e
        return

file_record_fdfs,celery = _init()

@app.task(bind=True)
def upload_new_file(self,source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route):
    global file_record_fdfs,celery
    try:
        cur_connection = _get_Connect_from_Pool(source_addr,source_port,user_name,passwd)

        ###############################
        # init the fdfs upload command#
        ###############################
        upload_file_cmd = 'fdfs_upload_file /etc/fdfs/client.conf {file_path}{file_name}'.\
                        format(file_path=file_path,file_name=file_name)
        stdin,stdout,stderr = cur_connection.exec_command(upload_file_cmd)
        out_message = stdout.readline()
        err_message = stderr.readline()
    except Exception as e:
        try:
            print Exception,":",e
            celery.send_task("async_html_update_service.upload_service.upload_new_file",
                    args=[source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route],
                    queue='upload_queue')
        except Exception as e:
            print "[ERROR]",cur_time,":","send back error"
            print Exception,":",e
        return

    #########################
    # get the execute result#
    #########################
    if err_message != "":
        cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        if "No such file or directory" in err_message:
            print "[Warning]",cur_time,":",err_message
            return
        else:
            print "[ERROR]",cur_time,":",err_message
            print "[RETRY]",cur_time
            try:
                celery.send_task("async_html_update_service.upload_service.upload_new_file",
                        args=[source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route],
                        queue='upload_queue')
            except Exception as e:
                print "[ERROR]",cur_time,":","send back error"
                print Exception,":",e
            return

    #####################################################################
    # upload sucess then remove it from local disk and insert the record#
    #####################################################################
    else:
        cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        i = file_record_fdfs.insert()
        try:
            file_store_id = out_message.replace('\n','')
            i.execute(create_time=cur_time,
                        file_name_full=file_path+file_name,
                        file_source_path=file_path,
                        file_name_shot=file_name,
                        source_address=source_addr,
                        file_store_id=file_store_id,
                        version_time=version_time,
                        source_route=source_route)
            delete_file_cmd = 'rm {file_path}{file_name}'.\
                        format(file_path=file_path,file_name=file_name)
            stdin,stdout,stderr = cur_connection.exec_command(delete_file_cmd)
            out_message = stdout.readline()
            err_message = stderr.readline()

            ##############################################        
            # remove fail and send task back to the queue#
            ##############################################
            if err_message != "":
                cur_time = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
                if "No such file or directory" in err_message:
                    print "[Warning]",cur_time,":",err_message
                    return
                else:
                    print "[ERROR]",cur_time,":",err_message
                    print "[RETRY]",cur_time
                    try:
                        ##############################################################
                        # roll back the task, try to remove the file from the Fastdfs#
                        ##############################################################
                        print "[ROLL BACK]",cur_time
                        delete_upload_file_cmd = 'fdfs_delete_file /etc/fdfs/client.conf {file_store_id}'.\
                                format(file_store_id=file_store_id)
                        stdin,stdout,stderr = cur_connection.exec_command(delete_upload_file_cmd)
                        if stderr == "":
                            celery.send_task("async_html_update_service.upload_service.upload_new_file",
                                    args=[source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route],
                                    queue='upload_queue')
                            print "[ROLL BACK SUCCESS]",cur_time
                        else:
                            print "[Warning]",cur_time,":",err_message
                            return
                    except Exception as e:
                        print "[ERROR]",cur_time,":","send back error"
                        print Exception,":",e
                    return
            else:
                print "[SUCCESS]",cur_time,":",'{%s:%s}'%(file_name,file_store_id)
        except Exception as e:
            try:
                print Exception,":",e
                ##############################################################
                # roll back the task, try to remove the file from the Fastdfs#
                ##############################################################
                print "[ROLL BACK]",cur_time
                delete_upload_file_cmd = 'fdfs_delete_file /etc/fdfs/client.conf {file_store_id}'.\
                        format(file_store_id=file_store_id)
                stdin,stdout,stderr = cur_connection.exec_command(delete_upload_file_cmd)
                if stderr == "":
                    celery.send_task("async_html_update_service.upload_service.upload_new_file",
                            args=[source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route],
                            queue='upload_queue')
                    print "[ROLL BACK SUCCESS]",cur_time
                else:
                    print "[Warning]",cur_time,":",err_message
                    return
            except Exception as e:
                print "[ERROR]",cur_time,":","send back error"
                print Exception,":",e
            return
