import json
import codecs
import MySQLdb
#import pysvn
import time

from celery import Celery

#************iniitialize insert option****************#


class AnjukePipeline(object):

	SVN_DATA_PATH = '/home/chiufung/fang_html/'

	def __init__(self):

		self.celery = Celery(broker="redis://192.168.6.10/2",backend="redis://192.168.6.10/3")
		
	def process_item(self, item, spider):
		
		host_name = 'fang'
		url = item['url']
		fang_id = item['fang_id']
		region_code = str(010)
		body = item['body']

		file_path = self.SVN_DATA_PATH
		file_name = '{0}_{1}_{2}.html'.format(host_name,region_code,fang_id)

		try:

			f = open(file_path+file_name,'w')
			f.write(body)
			f.close()

			source_addr = '192.168.6.10'
			source_port = 22
			user_name = 'chiufung'
			passwd = 'enzowcf'
			file_path = file_path
			file_name = file_name
			self.celery.send_task("async_html_update_service.upload_service.upload_new_file",
                    args=[source_addr,source_port,user_name,passwd,file_path,file_name],
                    queue='upload_queue')
		except Exception as e:
			print Exception,":",e

		return item

	#def spider_closed(self,spider):
	#	self.file.close()
