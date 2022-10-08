from anime_crawler.core.download import Downloader
from anime_crawler.core.imageio import ImageIO
from anime_crawler.core.requests_generator import RequestsGenerator
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.utils.options import Options
from anime_crawler.utils.stop_conditions import StopConditions
from anime_crawler.settings import *

'''
Engine类用于调度，主要有以下几个作用:

1. 让Downloader不断从RequestsRepository中pop出请求并完成下载(同时包含文件保存与数据库保存)

2. 检查停止/暂停条件，当满足停止条件时关闭爬虫；满足暂停条件时暂停爬虫；不满足时启动爬虫

3. 为ImageServer创建单独的运行环境

'''


class Engine:
    def __init__(self,
                 requests_generator_: RequestsGenerator,
                 stop_conditions: StopConditions,
                 requests_repository_: RequestsRepository,
                 filter_: BloomFilter,
                 downloader_: Downloader,
                 imageio_: ImageIO,
                 options_: Options) -> None:
        self._downloader = downloader_(requests_generator=requests_generator_,
                                       requests_repository=requests_repository_,
                                       imageio=imageio_,
                                       filter=filter_,
                                       options=options_)
        self._image_io = imageio_()
        self._stop_conditions = stop_conditions()

    @classmethod
    def run():
        ...

    def scheduler(self) -> None:
        # TODO 停止条件需要加入
        ...
