from redis import Redis
from anime_crawler.settings import REDIS_ADDR, REDIS_DB, REDIS_PORT, REDIS_TTL, REDIS_ENABLE, REDIS_PASSWD
from anime_crawler.utils.image_item import ImageItem
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.utils.fileio import FileIO


class ImageIO:
    def __init__(self) -> None:
        if REDIS_ENABLE:
            # redis连接
            self._connection = Redis(
                host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PASSWD, db=REDIS_DB)
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

        # TODO 先从数据库中读一个出来
        # 如果数据库为空，就从文件中读取，但是需要注意是否是已有的
        return ImageItem(*self._fileio.random_img())
