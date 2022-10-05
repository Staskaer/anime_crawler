from anime_crawler.utils.image_item import ImageItem
from requests import request, Request, Response
from anime_crawler.utils.decorator import run_async_c
from anime_crawler.utils.options import Options
from anime_crawler.settings import MAX_CONCURRENT_REQUESTS, MAX_RETRY, TIMEOUT
from anime_crawler.core.requests_reposity import RequestsReposity
from collections import deque


class Downloader:
    def __init__(self, requests_reposity: RequestsReposity, options: Options) -> None:
        self._count = 0  # 计算并发数目
        self._open = True  # 开启下载器
        self._requests_reposity = requests_reposity()  # requests库
        self._result = deque()  # 存储处理结果的列表

    def _callback(self, response: Response):
        '''
        是download的回调函数

        Args:
            response (response): 返回的response对象
        '''

        # TODO 关于名字的处理
        self._result.append(ImageItem(name="{}.{}".format(*response.url.strip("/").replace("/", ".").split(".")[-2:]),
                                      img=response.content))
        self._count -= 1

    @run_async_c(_callback)
    def _donwload(self, request_: Request):
        '''
        用于下载请求的函数，异步

        Args:
            request (request): request对象
        '''
        print(f"downloading {request_.url}，present downloads is {self._count}")
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
            except:
                ...

    def fill_download_queue(self) -> None:
        '''
        不断从requests库中取出requests对象直到填满并发数目
        '''
        while self._open and self._count < MAX_CONCURRENT_REQUESTS:
            if(self._result.__len__() > 20):
                print("now need to be release...")
                break
            self._count += 1
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

    def pop(self) -> ImageItem:
        '''
        获取一个item

        Returns:
            _type_: 返回下载的item
        '''
        # print(f"poping present items is {self._result.__len__()}")
        try:
            # TODO 可能出现没有下载完就请求pop
            return self._result.popleft()
        except:
            return None
