from anime_crawler.settings import REQUESTS_BATCH_SIZE
from requests import Request


class RequestsBlock:
    def __init__(self) -> None:
        self._batch_size = REQUESTS_BATCH_SIZE
        # TODO block简单的是列表可以被优化？
        self._block = []
        self._current_size = 0

    def _reset(self) -> None:
        '''
        清空内部数据
        '''
        self._current_size = 0
        self._block.clear()

    def append(self, request: Request) -> bool:
        '''
        添加一个request对象到RequestsBlock中，如果Block没有满就返回1否则返回0

        Args:
            request (_type_): request对象

        Returns:
            bool: 如果Block没有满就返回1否则返回0
        '''
        self._block.append(request)
        self._current_size += 1
        return True if self._current_size < self._batch_size else False

    def pop(self) -> Request:
        '''
        一个迭代器，负责从RequestsBlock中抽取Request对象

        Returns:
            Request: request对象

        Yields:
            Iterator[Request]: request对象
        '''
        yield from self._block
        self._reset()

    @property
    def batch_size(self) -> int:
        '''
        返回batchsize大小

        Returns:
            int: batchsize大小
        '''
        return self._batch_size
