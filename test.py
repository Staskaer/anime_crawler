from anime_crawler.core.download import Downloader
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.core.engine import Engine
from anime_crawler.core.imageio import ImageIO

# b = ImageIO()
# print(b.pop().name)

a = Downloader()
# i = 0
while 1:
    a.fill_download_queue()
    # i = (i+1) % 10
    # if i == 0:
    #     print(a._imageio.pop().name)
