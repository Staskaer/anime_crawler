from anime_crawler.utils.image_item import ImageItem
from requests import request, Request, Response
from anime_crawler.utils.decorator import run_async_c
from anime_crawler.utils.options import Options
from anime_crawler.settings import MAX_CONCURRENT_REQUESTS, MAX_RETRY, TIMEOUT
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.core.imageio import ImageIO


class Downloader:
    def __init__(self, requests_repository: RequestsRepository, imageio: ImageIO, options: Options) -> None:
        self._count = 0  # 计算并发数目
        self._open = True  # 开启下载器
        self._requests_repository = requests_repository()  # requests库
        self._imageio = imageio()  # image的接口

    def _callback(self, response: Response) -> None:
        '''
        是download的回调函数

        Args:
            response (response): 返回的response对象
        '''
        if response is None:
            # TODO 关于超时请求的处理
            print("超时")
            return

        # TODO 关于名字的处理
        name = "{}.{}".format(
            *response.url.strip("/").replace("/", ".").split(".")[-2:])
        self._imageio.add(ImageItem(name=name, img=response.content))
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
        return None

    def fill_download_queue(self) -> None:
        '''
        不断从requests库中取出requests对象直到填满并发数目
        '''
        while self._open and self._count < MAX_CONCURRENT_REQUESTS:
            # TODO 当generator生成速度不快的时候会导致此函数阻塞
            self._count += 1
            self._donwload(self._requests_repository.pop())

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
        # 关闭后不会影响到当前正在工作的下载任务
        self._open = False
