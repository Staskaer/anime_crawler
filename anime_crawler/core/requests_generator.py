from anime_crawler.http.requests_block import RequestsBlock
from random import randint
from requests import Request, get
from json import loads
from anime_crawler.settings import REQUESTS_BATCH_SIZE


class RequestsGenerator:
    def __init__(self) -> None:
        self.requests_block = RequestsBlock()
        self._size = 0

    def usr_generator(self) -> Request:
        url = "https://api.lolicon.app/setu/v2"
        paramrs = {
            "num": REQUESTS_BATCH_SIZE,
            "keyword": "百合"}
        while 1:
            r = get(url, paramrs, timeout=10)
            r = loads(r.text)
            items = r["data"]
            for item in items:
                for i in item["urls"].values():
                    yield Request("get", i)

    def generator_middleware(self) -> Request:
        '''
        请求生成器中间件

        Returns:
            Request: 处理统一的请求信息

        Yields:
            Iterator[Request]: 返回Request请求
        '''

        yield from self.usr_generator()

    def generator(self, batch_size: int) -> RequestsBlock:
        generate = self.generator_middleware()
        while self._size < batch_size:
            self._size += 1
            try:
                self.requests_block.append(next(generate))
            except StopIteration:
                break
        self._size = 0
        return self.requests_block
