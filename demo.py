# 导入engine和stopconditions！
from anime_crawler import StopConditions, Engine
# 导入自带的RequestsGenerator！
from anime_crawler import RequestsGenerator

# 实例化一个停止条件！
a = StopConditions()
# 添加停止条件，这里是爪巴取10分钟后停止呢！
a.add_stop_condition(lastingtime=10)
# 开始爪巴！
Engine.run(RequestsGenerator, a)

# 可以查看一下anime_crawler/settings.py的配置文件，可以自己修改一下哦！


# 上面是通用的运行方法哦，如果你只想简单的运行demo，可以直接运行下面的代码！

# Engine.run_default()
