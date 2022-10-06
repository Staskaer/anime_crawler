# anime_crawler
对动漫图片进行爬取的爬虫

---

预览版只需要把仓库拉下来然后执行`test.py`即可，目前的依赖项仅为`requests`库。

使用线程池来实现的requests库的多线程图片下载爬虫框架，如果需要自定义爬取图片，请直接修改`RequestsGnerator`这个类，也只需要修改这个类，爬虫的一些配置参考`settings.py`。

---

目前为预览版，功能还不够完善。