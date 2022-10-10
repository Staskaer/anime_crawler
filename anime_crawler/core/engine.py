from typing import Any
from time import sleep
from anime_crawler.core.download import Downloader
from anime_crawler.core.imageio import ImageIO
from anime_crawler.core.requests_generator import RequestsGenerator
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.utils.options import Options
from anime_crawler.utils.stop_conditions import StopConditions
from anime_crawler.utils.logger import Logger
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
                 stop_conditions: StopConditions(),
                 requests_repository_: RequestsRepository,
                 filter_: BloomFilter,
                 downloader_: Downloader,
                 imageio_: ImageIO,
                 options_: Options) -> None:
        self._logger = Logger("Engine")
        self._logger.info("初始化Engine")
        self._downloader = downloader_(requests_generator=requests_generator_,
                                       requests_repository=requests_repository_,
                                       imageio=imageio_,
                                       filter=filter_,
                                       options=options_)
        self._image_io = imageio_()
        self._stop_conditions = stop_conditions
        self._logger.info("Engine初始化完成")

    @classmethod
    def run(cls,
            generator: RequestsGenerator,
            stop_conditions: StopConditions = None,
            repository: RequestsRepository = RequestsRepository,
            filter_: BloomFilter = BloomFilter,
            downloader: Downloader = Downloader,
            imageio: ImageIO = ImageIO,
            options: Options = Options) -> Any:
        '''用于启动爬虫的类方法，用于创建Engine对象并启动爬虫'''
        if generator is None:
            raise ValueError("generator参数不能为空")
        if stop_conditions is None:
            stop_conditions = StopConditions()
        engine = Engine(
            requests_generator_=generator,
            stop_conditions=stop_conditions,
            requests_repository_=repository,
            filter_=filter_,
            downloader_=downloader,
            imageio_=imageio,
            options_=options
        )
        engine.scheduler()

    @classmethod
    def run_default(cls) -> Any:
        '''启用默认的爬虫类'''
        cls.run(RequestsGenerator, StopConditions(), RequestsRepository,
                BloomFilter, Downloader, ImageIO, Options)

    def scheduler(self) -> None:
        self._logger.warning("开始爬取")
        while 1:

            if not self._stop_conditions.valid():
                self._downloader.close()
                sleep(5)
                self._logger.warning("此次爬取停止")
                if not self._stop_conditions.get_circle():
                    self._logger.warning("爬虫已关闭，爬取结束")
                    break
                else:
                    self._logger.info("爬虫将在下一轮重新启动")
                    sleeptime = self._stop_conditions.get_sleep_time()
                    self._logger.warning("爬虫将在{}秒后重新启动".format(sleeptime))
                    sleep(sleeptime)
                    self._logger.warning("爬虫启动")
                    self._downloader.open()
                    self._stop_conditions.init()

            flag = self._downloader.fill_download_queue()
            if not flag:
                self._logger.warning("下载队列已空")
                self._logger.warning("关闭爬虫")
                break
