from redis import Redis
from anime_crawler.settings import (REDIS_ADDR,
                                    REDIS_DB,
                                    REDIS_PORT,
                                    REDIS_TTL,
                                    REDIS_ENABLE,
                                    REDIS_PASSWD,
                                    FILTER_ENABLE)
from anime_crawler.utils.image_item import ImageItem
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.utils.fileio import FileIO


class ImageIO:
    def __init__(self) -> None:
        if REDIS_ENABLE:
            # redis连接
            self._connection = Redis(
                host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PASSWD, db=REDIS_DB)
        if FILTER_ENABLE:
            self._bloom_filter = BloomFilter()  # 用于pop过滤
        self._fileio = FileIO()  # 文件读取接口

    def add(self, item: ImageItem) -> bool:
        '''
        将一个图像插入到数据库中，同时写入文件

        Args:
            item (ImageItem): 图像item

        Returns:
            bool: 是否成功
        '''
        print(f"parsing {item.name}")

        self._fileio.to_file(name=item.name, img=item.get_imgbytes())

        if REDIS_ENABLE:
            return self._connection.set(item.name, item.get_imgbase64(), ex=REDIS_TTL)
        else:
            return 1

    def pop(self) -> ImageItem:
        '''
        pop一个图片出来，这个函数不是线程安全的，不可重入

        Returns:
            ImageItem: 返回一个图像
        '''
        redis_times = 0
        if REDIS_ENABLE:
            print("pop from redis...")
            while 1:
                # 数目比较少或多次重复就的时候就break掉，防止阻塞
                if self._connection.dbsize()-redis_times < 10 or redis_times > 3:
                    break
                redis_times += 1
                key = self._connection.randomkey()
                try:
                    value = self._connection.get(key)
                except:
                    continue
                if FILTER_ENABLE and not self._bloom_filter.find(key):
                    self._bloom_filter.add(key)
                    return ImageItem(key, base64=value.decode("utf-8"))
                if not FILTER_ENABLE:
                    return ImageItem(key, base64=value.decode("utf-8"))

        # 如果缓存处失败，就从文件中读取
        print("pop from file...")
        while 1:
            name, img_b = self._fileio.random_img()
            if FILTER_ENABLE and not self._bloom_filter.find(name):
                self._bloom_filter.add(name)
                return ImageItem(name, img=img_b)
            if not FILTER_ENABLE:
                return ImageItem(name, img=img_b)
