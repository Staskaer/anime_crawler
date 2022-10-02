from requests import get, Request, Response
from anime_crawler.utils.decorator import run_async_c
from anime_crawler.utils.options import Options
from anime_crawler.settings import MAX_CONCURRENT_REQUESTS, MAX_RETRY
from .requests_reposity import RequestsReposity
from collections import deque

# TODO 补全日志结构


class Downloader:
    def __init__(self, requests_reposity: RequestsReposity, options: Options) -> None:
        self._count = 0  # 计算并发数目
        self._open = True  # 开启下载器
        self._requests_reposity = requests_reposity  # requests库
        self._result = deque()  # 存储处理结果的列表

    def _callback(self, response: Response):
        '''
        是download的回调函数

        Args:
            response (response): 返回的response对象
        '''
        # TODO 回调函数处理返回对象并解析出图像
        self.count -= 1
        if self._open == True:
            self.fill_download_queue()

    @run_async_c(_callback)
    def _donwload(self, request: Request):
        '''
        用于下载请求的函数，异步

        Args:
            request (request): request对象
        '''
        self.count += 1

        for i in range(MAX_RETRY):  # 会重试几次
            try:
                response = get(request)
                return response
            except:
                ...

    def fill_download_queue(self) -> None:
        '''
        不断从requests库中取出requests对象直到填满并发数目
        '''
        while self.count <= MAX_CONCURRENT_REQUESTS:
            self._donwload(self._requests_reposity.pop())

    def open(self) -> None:
        '''
        开启downloader
        '''
        if self._open != True:
            self._open = True
            self.fill_download_queue()

    def close(self) -> None:
        '''
        关闭downloader
        '''
        self._open = False

    def pop(self):

        return self._result.popleft()