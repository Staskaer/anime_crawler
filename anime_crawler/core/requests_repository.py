from anime_crawler.http.requests_block import RequestsBlock
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.core.requests_generator import RequestsGenerator
from collections import deque
from requests import Request
from anime_crawler.settings import REQUESTS_BATCH_SIZE
from anime_crawler.utils.logger import Logger


class RequestsRepository:
    def __init__(self,
                 requests_generator_: RequestsGenerator = RequestsGenerator,
                 filter: BloomFilter = BloomFilter) -> None:
        '''
        构造函数，通过requests_generator和filter来构造出requests_repository

        Args:
            requests_generator_ (RequestsGenerator, optional): requests_generator，需要自己提供或使用默认. Defaults to RequestsGenerator.
            filter (BloomFilter, optional): 过滤器，默认为布隆过滤器. Defaults to BloomFilter.
        '''
        self._logger = Logger("RequestsRepository")
        self._logger.info("初始化RequestsRepository")
        self._filter = filter()  # 去重用的布隆过滤器
        self._queue = deque()  # request对象列表
        self._count = 0  # 队列中的元素
        self.requests_generator = requests_generator_()  # requests生成器
        # TODO 将这个目前使用返回值的东西修正成生成器
        self.append(self.requests_generator.generator(REQUESTS_BATCH_SIZE*4))
        self._logger.info("RequestsRepository初始化完成")

    def pop(self) -> Request:
        '''
        pop出一个Request对象

        Returns:
            Request: 一个Request对象，用于downloader
        '''
        # 先判断是否需要生成一批request对象
        if self._count < REQUESTS_BATCH_SIZE:
            self.append(self.requests_generator.generator(REQUESTS_BATCH_SIZE))

        self._count -= 1
        return self._queue.popleft()

    def append(self, requests_blcoks: RequestsBlock) -> bool:
        '''
        将一个batchsize的requestsblock添加到队列中

        Args:
            requests_blcoks (RequestsBlock): requestsblocks

        Returns:
            bool: 成功返回1否则为0
        '''
        for request in requests_blcoks.pop():
            if not self._filter.find(request.url):
                self._filter.add(request.url)
                self._queue.append(request)
                self._count += 1
        return True
