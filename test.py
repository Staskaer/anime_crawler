from anime_crawler.core.download import Downloader
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.bloomfilter import BloomFilter
from anime_crawler.core.engine import Engine
from anime_crawler.core.imageio import ImageIO

a = Downloader(RequestsRepository, ImageIO, None)
while 1:
    a.fill_download_queue()
