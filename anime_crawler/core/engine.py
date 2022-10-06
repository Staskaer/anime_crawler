from anime_crawler.core.download import Downloader
from anime_crawler.core.imageio import ImageIO
from anime_crawler.core.requests_repository import RequestsRepository
from anime_crawler.utils.image_item import ImageItem
from anime_crawler.settings import *
from anime_crawler.utils.options import Options
from anime_crawler.utils.stop_conditions import StopConditions

# TODO 目前没用


class Engine:
    def __init__(self) -> None:
        self._downloader = Downloader(RequestsRepository, Options)
        self._imageio = ImageIO()

    def scheduler(self, stop: StopConditions) -> None:
        # TODO 停止条件需要加入
        while 1:
            self._downloader.fill_download_queue()
            if ((item := self._downloader.pop()) is None):
                continue
            self._imageio.add(item)
