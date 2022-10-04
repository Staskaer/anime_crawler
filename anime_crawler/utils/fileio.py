import os
from anime_crawler.settings import FILE_PATH
from random import randint


class FileIO:
    def __init__(self) -> None:
        self._path = FILE_PATH

    def to_file(self, img: bytes, name: str) -> bool:
        '''
        将图像持久化到文件函数

        Args:
            img (bytes): 字节格式的图片
            name (str): 图片名称

        Returns:
            bool: 是否写入成功
        '''
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        while os.path.exists(os.path.join(self._path, name)):
            # 保证当前图像名不被占用
            if("." in name):
                name = "{}_.{}".format(*name.split("."), randint(1, 1e5))
            else:
                name += f"_{randint(1,1e5)}.jpg"
        # 下面写入文件
        with open(os.path.join(self._path, name), "wb") as f:
            f.write(img)
        return True

    def from_file(self, name: str) -> bytes:
        '''
        从文件中读取图像

        Args:
            name (str): 文件名称

        Returns:
            bytes: 图像的字节流
        '''
        if os.path.exists(os.path.join(self._path, name)):
            with open(os.path.join(self._path, name), "rb") as f:
                # TODO 这是否是正确的字节流呢？
                img = f.read()
            return img
