from anime_crawler.core.download import Downloader
from anime_crawler.core.imageio import ImageIO
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.image_item import ImageItem
from anime_crawler.settings import *
from anime_crawler.utils.options import Options
from anime_crawler.utils.stop_conditions import StopConditions

'''
Engine类用于调度，主要有以下几个作用:

1. 让Downloader不断从RequestsRepository中pop出请求并完成下载(同时包含文件保存与数据库保存)

2. 检查停止/暂停条件，当满足停止条件时关闭爬虫；满足暂停条件时暂停爬虫；不满足时启动爬虫

3. 为ImageServer创建单独的运行环境

'''


class Engine:
    def __init__(self,
                 requests_repository: RequestsRepository,
                 downloader: Downloader,
                 requests_generator) -> None:
        self._downloader = downloader()
        self._imageio = ImageIO()

    def scheduler(self, stop: StopConditions) -> None:
        # TODO 停止条件需要加入
        while 1:
            self._downloader.fill_download_queue()
            if ((item := self._downloader.pop()) is None):
                continue
            self._imageio.add(item)
