from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from os.path import splitext
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        list_to_return = [Request(i, meta={'filename': item.get('file_name')})
                          for i in item.get(self.files_urls_field, [])]
        return list_to_return

    def file_path(self, request, response=None, info=None):
        url = request.url
        media_ext = splitext(url)[1] # url.split('.')[-1]x
        return f'full\\{request.meta["filename"]}{media_ext}'

