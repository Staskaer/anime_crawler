from concurrent.futures import ThreadPoolExecutor
from anime_crawler.settings import MAX_CONCURRENT_REQUESTS

pool = ThreadPoolExecutor(MAX_CONCURRENT_REQUESTS)


def run_async_c(callback):
    '''
    装饰器，可以将同步函数转变为异步函数，其中返回值会被calllback处理，但是需要保证是类成员函数

    Args:
        callback (function): 处理返回值的回调函数
    '''
    def inner(func):
        def wrapper(*args, **kwargs):
            def __exec():
                out = func(*args, **kwargs)
                callback(args[0], out)  # args[0]是self
                return out
            pool
            return pool.submit(__exec)
        return wrapper
    return inner
