from base64 import b64encode, b64decode
from anime_crawler.settings import REDIS_ENABLE


class ImageItem:
    def __init__(self,  name: str, img: bytes = None, base64: str = None) -> None:
        '''
        构造函数

        Args:
            name (str): 图像名字
            img (bytes, optional): 二进制格式的图像. Defaults to None.
            base64 (str, optional): 字符串格式的base64编码. Defaults to None.

        '''
        self.name = name
        if img is not None:
            if REDIS_ENABLE:
                base64_data = b64encode(img)
                self.base64 = str(base64_data, 'utf-8')
            self.imgbytes = img
        if REDIS_ENABLE:
            if base64 is not None:
                self.imgbytes = b64decode(base64)
                self.base64 = base64
        if img is None and base64 is None:
            self.imgbytes = None
            self.base64 = None

    def add_img(self, img: bytes) -> None:
        '''
        为item添加图像

        Args:
            img (bytes): 二进制格式的图像
        '''
        self.imgbytes = img
        if REDIS_ENABLE:
            base64_data = b64encode(img)
            self.base64 = str(base64_data, 'utf-8')

    def add_base64(self, base64: str) -> None:
        '''
        为item添加base64编码

        Args:
            base64 (str): 字符串的base64编码
        '''
        if REDIS_ENABLE:
            self.base64 = base64
        self.imgbytes = b64decode(base64)

    def get_imgbytes(self) -> bytes:
        '''
        获取二进制格式图片

        Returns:
            bytes: 图片的二进制格式
        '''
        return self.imgbytes

    def get_imgbase64(self) -> str:
        '''
        获取图像的base64

        Returns:
            str: 图像的base64编码
        '''
        if REDIS_ENABLE:
            return self.base64
        raise Exception("Redis is not enable")
