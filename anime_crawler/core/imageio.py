from redis import Redis
from anime_crawler.settings import REDIS_ADDR, REDIS_DB, REDIS_PORT, REDIS_TTL, REDIS_PASSWD
from anime_crawler.utils.image_item import ImageItem
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.utils.fileio import FileIO


class ImageIO:
    def __init__(self) -> None:
        self._connection = Redis(
            host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PASSWD, db=REDIS_DB)
        self._bloom_filter = BloomFilter()
        self._fileio = FileIO()

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

        return 1
        # return self._connection.set(item.name, item.get_imgbase64(), ex=REDIS_TTL)

    def pop(self) -> ImageItem:
        ...
        # TODO 先从数据库中读一个出来
        # 如果数据库为空，就从文件中读取，但是需要注意是否是已有的
