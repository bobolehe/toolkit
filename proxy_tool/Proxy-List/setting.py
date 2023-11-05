# 获取代理目标
import datetime

HTTP_LIST = [
    "https://openproxylist.xyz/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://rootjazz.com/proxies/proxies.txt",
    # "https://sheesh.rip/http.txt",
    # "https://www.proxyscan.io/download?type=http"
]

# 使用线程或进程
T_OR_P = True
# 线程数量
NUM_THREADS = 10
# 进程数量
NUM_PROCESSES = 10

# 备选获取代理目标
you = [
    "https://openproxy.space/list/http", "https://spys.me/proxy.txt",
]

# 写入json文件配置
js_switch = False
date = datetime.datetime.now()
JSON_FILE = f"./json/http-{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}.json"

# redis配置
redis_switch = True
redis_config = {
    "HOST": "127.0.0.1",
    "PORT": 6379,
    "PASSWORD": "123456",
    "DB": 0,
}
