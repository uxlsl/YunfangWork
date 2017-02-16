from scrapy.core.downloader.webclient import ScrapyHTTPClientFactory, ScrapyHTTPPageGetter
class PageGetter(ScrapyHTTPPageGetter):
    def sendCommand(self, command, path):
        self.transport.write('%s %s HTTP/1.1\r\n' % (command, path))
class HTTPClientFactory(ScrapyHTTPClientFactory):
     protocol = PageGetter