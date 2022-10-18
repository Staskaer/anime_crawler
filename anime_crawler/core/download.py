from anime_crawler.utils.image_item import ImageItem
from anime_crawler.utils.bloomfilter import BloomFilter
from requests import request, Request, Response
from anime_crawler.utils.decorator import run_async_c
from anime_crawler.utils.options import Options
from anime_crawler.settings import (MAX_CONCURRENT_REQUESTS,
                                    MAX_RETRY,
                                    TIMEOUT,
                                    DELAY_AFTER_REQUEST)
from anime_crawler.core.requests_generator import RequestsGenerator
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.core.imageio import ImageIO
from anime_crawler.utils.logger import Logger
from time import sleep


class Downloader:
    def __init__(self,
                 requests_generator: RequestsGenerator = RequestsGenerator,
                 requests_repository: RequestsRepository = RequestsRepository,
                 imageio: ImageIO = ImageIO,
                 filter: BloomFilter = BloomFilter,
                 options: Options = None) -> None:
        '''
        使用requests_repository和imageio来构建downloader，其中requests_generator和filter用于构建requests_repository

        Args:
            requests_generator (RequestsGenerator, optional): requests_generator，用于生成requests_repository. Defaults to RequestsGenerator.
            requests_repository (RequestsRepository, optional): requests_repository类. Defaults to RequestsRepository.
            imageio (ImageIO, optional): ImageIO接口类. Defaults to ImageIO.
            filter (BloomFilter, optional): 用于requests_repository的过滤器类. Defaults to BloomFilter.
            options (Options, optional): 选项，暂时无用. Defaults to None.
        '''
        self._logger = Logger("Downloader")
        self._logger.info("初始化Downloader")
        self._count = 0  # 计算并发数目
        self._open = True  # 开启下载器
        self._requests_repository = requests_repository(
            requests_generator, filter)  # requests库
        self._imageio = imageio()  # image的接口
        self._logger.info("Downloader初始化完成")

    def _callback(self, response: Response) -> None:
        '''
        是download的回调函数

        Args:
            response (response): 返回的response对象
        '''
        try:
            if response is None:
                # TODO 关于超时请求的处理
                # self._logger.error("response is None")
                return
            # TODO 关于名字的处理
            name = "{}.{}".format(
                *response.url.strip("/").replace("/", ".").split(".")[-2:])
            self._imageio.add(ImageItem(name=name, img=response.content))
            self._count -= 1
            sleep(DELAY_AFTER_REQUEST)
        except Exception as e:
            self._logger.error("处理时出错，疑似兼容性bug，错误信息:{}".format(e))

    @run_async_c(_callback)
    def _donwload(self, request_: Request):
        '''
        用于下载请求的函数，异步

        Args:
            request (request): request对象
        '''
        self._logger.info("开始下载{}，目前并发数目为{}".format(request_.url, self._count))
        # TODO 下载失败的错误
        for i in range(MAX_RETRY):  # 会重试几次
            try:
                response = request(request_.method,
                                   request_.url,
                                   params=request_.params,
                                   data=request_.data,
                                   json=request_.json,
                                   headers=request_.headers,
                                   cookies=request_.cookies,
                                   files=request_.files,
                                   auth=request_.auth,
                                   timeout=TIMEOUT
                                   )
                return response
            except Exception as e:
                self._logger.warning(
                    "下载{}失败，重试第{}次，出错原因{}".format(request_.url, i+1, e))

        self._logger.error("下载{}失败，放弃下载".format(request_.url))
        return None

    def fill_download_queue(self) -> None:
        '''
        不断从requests库中取出requests对象直到填满并发数目
        '''
        add_count = 0
        while self._open and self._count < MAX_CONCURRENT_REQUESTS and add_count < MAX_CONCURRENT_REQUESTS/2:
            # TODO 当generator生成速度不快的时候会导致此函数阻塞
            # 目前的解决方案是一次调用有最多添加任务数目的限制
            self._count += 1
            add_count += 1
            try:
                req = self._requests_repository.pop()
            except StopIteration:
                self._logger.warning(
                    "requests_repository为空，关闭downloader，等待下一次开启")
                self.close()
                return False
            except Exception as e:
                self._logger.error("requests_repository出错，错误信息:{}".format(e))
                self.close()
                return False
            self._donwload(req)
        return True

    def open(self) -> None:
        '''
        开启downloader
        '''
        if self._open is not True:
            self._logger.info("downloader已经开启")
            self._open = True
            self.fill_download_queue()

    def close(self) -> None:
        '''
        关闭downloader
        '''
        # 关闭后不会影响到当前正在工作的下载任务
        self._logger.info("downloader已经关闭")
        self._open = False
