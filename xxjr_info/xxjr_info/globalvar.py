class GlobalVar: 

	CUR_SPIDER_ID = 0 
	CUR_SPIDER_COUNT = 1

	def set_spider_id(self,num): 
		self.CUR_SPIDER_ID = num

	def spider_id_add(self): 
		self.CUR_SPIDER_ID = self.CUR_SPIDER_ID + 1

	def get_spider_id(self): 
		return self.CUR_SPIDER_ID 

	def get_spider_count(self): 
		return self.CUR_SPIDER_COUNT