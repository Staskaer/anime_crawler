from anime_crawler.utils.fileio import FileIO


class StopConditions:
    def __init__(self, fileio_: FileIO = FileIO) -> None:
        self._lasttingtime = None  # 持续时间(min):int
        self._size_of_pics = None  # 占用空间(MB):int
        self._nums = None  # 下载的数目
        self._timerange = None  # 给定运行时间

        self._circle = True  # 是否重复执行
        self._fileio = fileio_()  # FileIO接口

        self._start_time = 0  # 用于判断的变量
        self._last_nums = 0
        self._last_size = 0

    def valid(self) -> bool:
        '''
        验证是否到达停止条件

        Returns:
            bool: 停止返回1，否则返回0
        '''
        if self._circle is False:
            ...
        else:
            ...

    def add_stop_conditions(self, type_=""):
        ...
