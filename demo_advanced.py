from anime_crawler import RequestsGenerator, StopConditions, Engine
from requests import Request, get
from json import loads


# 需要继承自RequestsGenerator并重写usr_generator函数即可
class myGnerator(RequestsGenerator):
    def __init__(self) -> None:
        super().__init__()

    def usr_generator(self) -> Request:
        '''
        这是一个生成器，用于生成Request对象

        Returns:
            Request: 

        Yields:
            Iterator[Request]: 返回Request请求
        '''

        # 这里放你的爬取逻辑，每次yield一个Request对象
        yield Request("get", "https://www.baidu.com")

        # 你可以把下面这个注释取消来试一下

        # url = "https://api.lolicon.app/setu/v2"
        # paramrs = {
        #     "num": 16,
        #     "keyword": "白丝"}
        # while 1:
        #     r = get(url, paramrs, timeout=10)
        #     r = loads(r.text)
        #     items = r["data"]
        #     for item in items:
        #         for i in item["urls"].values():
        #             yield Request("get", i)

    def generator_middleware(self) -> Request:
        '''
        这是中间键，用于预处理Request对象，比如添加headers，cookies等
        如果你不需要这个功能，可以不修改这个函数
        这个函数默认的功能是什么都不做，像下面这样
        '''
        yield from self.usr_generator()


if __name__ == "__main__":
    # 运行方法和之前一致
    a = StopConditions()
    a.add_stop_condition(lastingtime=10)
    Engine.run(myGnerator, a)
