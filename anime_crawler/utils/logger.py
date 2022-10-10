from anime_crawler.settings import LOG_LEVEL
from time import strftime, localtime

log_dict = {
    "INFO": 0,
    "WARNING": 1,
    "ERROR": 2
}


class Logger:
    def __init__(self, name: str) -> None:
        self._log_level = log_dict[LOG_LEVEL.upper()]
        self._name = name
        self._format = "{} [{}]-{} {}"
        # 输出形如"2022-10-9 12:12:12 [INFO]-engine 信息内容"

    def info(self, msg: str) -> None:
        if self._log_level <= log_dict["INFO"]:
            print(self._format.format(self._get_time(), "INFO", self._name, msg))

    def warning(self, msg: str) -> None:
        if self._log_level <= log_dict["WARNING"]:
            print(self._format.format(self._get_time(), "WARNING", self._name, msg))

    def error(self, msg: str) -> None:
        if self._log_level <= log_dict["ERROR"]:
            print(self._format.format(self._get_time(), "ERROR", self._name, msg))

    @staticmethod
    def _get_time() -> str:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
