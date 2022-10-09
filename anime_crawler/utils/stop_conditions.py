from anime_crawler.utils.fileio import FileIO
from datetime import datetime, timedelta
from anime_crawler.utils.logger import Logger


class StopConditions:
    def __init__(self,  circle_: bool = True, fileio_: FileIO = FileIO) -> None:
        self._logger = Logger("StopConditions")
        self._logger.info("初始化StopConditions")
        self._lasttingtime = None  # 持续时间(min):int
        self._size_of_pics = None  # 占用空间(MB):float
        self._nums = None  # 下载的数目
        self._timerange = None  # 给定运行时间

        self._circle = circle_  # 是否重复执行
        self._fileio = fileio_()  # FileIO接口

        self.init()

        self._logger.info("StopConditions初始化完成")

    def init(self) -> None:
        '''
        初始化，用于获取初始值，每次重启后都要先调用这个
        '''
        self._logger.warning("StopConditions正在装载初始值")
        self._start_time = datetime.now()
        self._start_nums = self._fileio.get_nums()
        self._start_size = self._fileio.get_size()
        self._logger.warning("StopConditions初始值装载完成")

    def valid(self) -> bool:
        '''
        判断是否满足停止条件

        Returns:
            bool: 是否满足停止条件
        '''

        if self._circle is True:
            if self._lasttingtime is not None:
                if self._calculate_delta_time() >= self._lasttingtime:
                    self._logger.warning("已达到持续时间条件，准备关闭downloader")
                    return False
            if self._size_of_pics is not None:
                if self._calculate_delta_size() >= self._size_of_pics:
                    self._logger.warning("已达到占用空间条件，准备关闭downloader")
                    return False
            if self._nums is not None:
                if self._calculate_delta_nums() >= self._nums:
                    self._logger.warning("已达到下载数目条件，准备关闭downloader")
                    return False
            if self._timerange is not None:
                if not self._is_in_time(datetime.now()):
                    self._logger.warning("已达到给定运行时间条件，准备关闭downloader")
                    return False
            return True
        else:
            if self._lasttingtime is not None:
                if self._calculate_delta_time() >= self._lasttingtime:
                    self._logger.warning("已达到持续时间条件，准备关闭downloader")
                    # TODO 定义异常类
                    raise StopIteration
            if self._size_of_pics is not None:
                if self._calculate_delta_size() >= self._size_of_pics:
                    self._logger.warning("已达到占用空间条件，准备关闭downloader")
                    raise StopIteration
            if self._nums is not None:
                if self._calculate_delta_nums() >= self._nums:
                    self._logger.warning("已达到下载数目条件，准备关闭downloader")
                    raise StopIteration
            if self._timerange is not None:
                if not self._is_in_time(datetime.now()):
                    self._logger.warning("已达到给定运行时间条件，准备关闭downloader")
                    raise StopIteration
            return True

    def add_stop_condition(self,
                           lastingtime: float = None,
                           size_of_pics: float = None,
                           nums: int = None,
                           timerange: str = None) -> None:
        '''
        添加停止条件

        Args:
            lastingtime (int, optional): 持续时间，单位为min. Defaults to None.
            size_of_pics (int, optional): 占用空间，单位为MB. Defaults to None.
            nums (int, optional): 下载的数目，单位为个. Defaults to None.
            timerange (str, optional): 给定运行时间，是一个区间，在此区间内运行. Defaults to None.

            举例:timerange = '10:00-14:00'，表示在10:00-14:00之间运行，且每天都会在这个区间内运行程序.
            另外，此条件可以和其他条件结合执行，比如
            1. lastingtime=10，timerange='10:00-14:00'表示每天10点开启运行，运行时间10分钟
            2. size_of_pics=100，timerange='10:00-14:00'表示每天10点开启运行，直到爬取满100MB的图
            3. nums=100，timerange='10:00-14:00'表示每天10点开启运行，直到爬取满100张图
            4. lastingtime=10，size_of_pics=100，timerange='10:00-14:00'表示每天10点开启运行，运行时间10分钟或者直到爬取满100MB的图

        '''
        if lastingtime is not None:
            self._lasttingtime = lastingtime
        if size_of_pics is not None:
            self._size_of_pics = size_of_pics
        if nums is not None:
            self._nums = nums
        if timerange is not None:
            try:
                start_time, end_time = timerange.split('-')

                # 这里用了一个闭包来实现
                def _is_in_time(starttime, endtime):
                    def comp(time: datetime) -> bool:
                        datestr = "{}-{}".format(time.hour, time.minute)
                        return starttime <= datestr <= endtime
                    return comp
                self._is_in_time = _is_in_time(start_time, end_time)
            except ValueError:
                print('timerange参数错误，正确格式应该形如"10:00-14:00"')

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
