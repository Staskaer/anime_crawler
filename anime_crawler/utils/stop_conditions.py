from anime_crawler.utils.fileio import FileIO
from datetime import datetime, timedelta


class StopConditions:
    def __init__(self, fileio_: FileIO = FileIO) -> None:
        self._lasttingtime = None  # 持续时间(min):int
        self._size_of_pics = None  # 占用空间(MB):int
        self._nums = None  # 下载的数目
        self._timerange = None  # 给定运行时间

        self._circle = True  # 是否重复执行
        self._fileio = fileio_()  # FileIO接口

        self._start_time = datetime.now()  # 用于判断的变量
        self._start_nums = 0
        self._start_size = 0

    def valid(self) -> bool:
        '''
        判断是否满足停止条件

        Returns:
            bool: 是否满足停止条件
        '''
        if self._lasttingtime is not None:
            if self._calculate_delta_time() >= self._lasttingtime:
                return False
        if self._size_of_pics is not None:
            if self._calculate_delta_size() >= self._size_of_pics:
                return False
        if self._nums is not None:
            if self._calculate_delta_nums() >= self._nums:
                return False

        return True

    def add_stop_condition(self, condition: str, value: int) -> None:
        '''
        添加停止条件

        Args:
            condition (str): 停止条件，可选值为lastingtime,size_of_pics,nums,timerange
            value (int): 值，单位为分钟，MB，个数，时间范围
        '''
        if condition == 'lastingtime':
            self._lasttingtime = timedelta(minutes=value)
        elif condition == 'size_of_pics':
            self._size_of_pics = value
        elif condition == 'nums':
            self._nums = value
        elif condition == 'timerange':
            self._timerange = value
        else:
            raise ValueError('Invalid stop condition')

    def delete_stop_condition(self, condition: str) -> None:
        '''
        删除停止条件

        Args:
            condition (str): 停止条件，可选值为lastingtime,size_of_pics,nums,timerange
        '''
        if condition == 'lastingtime':
            self._lasttingtime = None
        elif condition == 'size_of_pics':
            self._size_of_pics = None
        elif condition == 'nums':
            self._nums = None
        elif condition == 'timerange':
            self._timerange = None
        else:
            raise ValueError('Invalid stop condition')

    def _calculate_delta_time(self) -> float:
        '''
        计算起始时间与当前时间的差值

        Returns:
            float: 返回差值，单位为分钟
        '''
        return (datetime.now() - self._start_time).total_seconds()/60

    def _calculate_delta_size(self) -> float:
        '''
        计算起始大小与当前大小的差值

        Returns:
            float: 返回差值，单位为MB
        '''
        return (self._fileio.get_size() - self._start_size)/1024/1024

    def _calculate_delta_nums(self) -> int:
        '''
        计算起始数目与当前数目的差值

        Returns:
            int: 返回差值
        '''
        return self._fileio.get_nums() - self._start_nums
