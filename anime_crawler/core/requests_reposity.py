from anime_crawler.http.requests_block import RequestsBlock
from anime_crawler.utils.bloomfilter import BloomFilter
from collections import deque
from requests import Request


class RequestsReposity:
    def __init__(self) -> None:
        self._filter = BloomFilter()  # 去重用的布隆过滤器
        self._queue = deque()  # request对象列表
        self._count = 0  # 队列中的元素

    def pop(self) -> Request:
        '''
        pop出一个Request对象

        Returns:
            Request: 一个Request对象，用于downloader
        '''
        # TODO 先判断是否需要生成一批request对象

        return self._queue.popleft()

    def append(self, requests_blcoks: RequestsBlock) -> bool:
        '''
        将一个batchsize的requestsblock添加到队列中

        Args:
            requests_blcoks (RequestsBlock): requestsblocks

        Returns:
            bool: 成功返回1否则为0
        '''
        for request in requests_blcoks:
            # TODO 感觉这里不对，应该是把网址放进去而不是把对象放进去
            if not self._filter.find(request):
                self._filter.add(request)
                self._queue.append(request)
                self._count += 1
        return True
