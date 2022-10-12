# anime_crawler的配置文件

##########全局配置##########

# 日志等级 "INFO", "WARNING", "ERROR"。建议为INFO，后两者信息太烧了。
LOG_LEVEL = "INFO"


##########Downloader类的配置项##########

# 下载器的最大并发数目
MAX_CONCURRENT_REQUESTS = 16

# 每个请求后的延迟时间(单位为秒)(建议不要太低)
DELAY_AFTER_REQUEST = 3

# 每个请求最多重试次数
MAX_RETRY = 3

# timeout
TIMEOUT = 30

##########RequestsRepository类的配置项##########

# Requests_block的大小
REQUESTS_BATCH_SIZE = 16

# 程序启动时初始生成的Requests_block数目
START_REQUESTS_BLOCKS = 4

##########BloomFilter类的配置项##########

# 每个过滤器容量
BLOOM_FILTER_CAPACITY = 1e5

# 每个过滤器的错误率
BLOOM_FILTER_ERROR = 0.001

##########ImageIO类的配置项##########

# 开启redis数据库(默认关闭，不建议开启捏)
REDIS_ENABLE = False

# redis数据库地址
REDIS_ADDR = "127.0.0.1"

# redis数据库端口
REDIS_PORT = 6379

# redis数据库的db
REDIS_DB = 0

# redis数据库的密码
REDIS_PASSWD = "root"

# 过期时间(秒)
REDIS_TTL = 120

# 文件图片的保存路径
# FILE_PATH = "/mnt/hdd/images/"
FILE_PATH = "D://animal/"

# 是否在pop时启用去重(建议关闭)
FILTER_ENABLE = False
