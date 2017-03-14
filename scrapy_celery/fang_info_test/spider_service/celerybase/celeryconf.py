broker_url = "redis://192.168.6.4:6379/2"
result_backend = "redis://192.168.6.4:6379/3"
include = ['spider_service.services.spider_service',]
task_default_queue = 'celery_spider_queue'