from anime_crawler.core.download import Downloader
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.core.engine import Engine
from anime_crawler.core.imageio import ImageIO
from anime_crawler.utils.logger import Logger

# c = Logger("test")
# c.info("info")
# c.warning("warning")
# c.error("error")

# b = ImageIO()
# print(b.pop().name)

a = Downloader()
while 1:
    a.fill_download_queue()
