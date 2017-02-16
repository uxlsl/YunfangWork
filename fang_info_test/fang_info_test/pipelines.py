import logging
import json
import codecs
import MySQLdb
#import pysvn
import time
import fang_info_test.log_mysql as log_mysql
import random

from celery import Celery

logger = logging.getLogger(__name__)

#************iniitialize insert option****************#


class Fang_Info_Test_Pipeline(object):

    SVN_DATA_PATH = '/home/chiufung/fang_html/'

    def __init__(self):

        self.celery = Celery(broker="redis://192.168.6.4/2",backend="redis://192.168.6.4/3")
        
    def process_item(self, item, spider):
        
        host_name = 'fang'
        url = item['url']
        fang_id = item['fang_id']
        region_code = '010'
        body = item['body']
        version_time = item['version_time']
        source_route = item['source_route']

        file_path = self.SVN_DATA_PATH
        file_name = '{0}_{1}_{2}_{3}_{4}.html'.format(host_name,region_code,fang_id,version_time,str(random.randint(1,60)))

        try:

            f = open(file_path+file_name,'w')
            f.write(body)
            f.close()

            source_addr = '192.168.6.204'
            source_port = 22
            user_name = 'chiufung'
            passwd = 'enzowcf'
            file_path = file_path
            file_name = file_name
            self.celery.send_task("async_html_update_service.upload_service.upload_new_file",
                    args=[source_addr,source_port,user_name,passwd,file_path,file_name,version_time,source_route],
                    queue='upload_queue')
            log_mysql.log_in_mysql(url,'Crawl success')
            logger.debug('Crawl success')
        except Exception as e:
            print Exception,":",e

        return item

    #def spider_closed(self,spider):
    #    self.file.close()
