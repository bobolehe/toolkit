import datetime
from urllib.parse import quote_plus as urlquote

# redis配置
redis_switch = True
redis_config = {
    "HOST": "127.0.0.1",
    "PORT": 6379,
    "DB": 0,
}
# check_proxy配置
check = {
    'checkerproxy_proxy': True,
    'english_proxy': False,
    'free_proxy': False,
    'geonode_proxy': True,
    'kuaidaili_proxy': True,
    'kuaidaili2_proxy': True,
    'openproxy_proxy': True,
    'spys_proxy': True,
    'rootjazz_proxy': True,
    'proxyspace_proxy': True,
    'proxylistplus_proxy': False,
}


class BaseConfig:
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
        "USERNAME": "default",
        "DB": 0,
    }
    # 权限是否启用
    RIGHTS = False  # 是否启用权限
    RIGHTS_GET = 'key'  # 接收权限验证参数名
    RIGHTS_KEY = '7ujm,lp-='  # 允许访问密钥

    SECRET_KEY = "pear-admin-flask"
    # JWT密钥
    JWT_SECRET_KEY = 'JwTOn1'
    # JWT有效期 通过redis进行管理则无需设置管理时间
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    # redis配置
    host = redis_config["HOST"]  # redis服务地址
    port = redis_config["PORT"]  # redis服务端口
    password = redis_config["PASSWORD"]  # redis服务密码
    db = redis_config["DB"]  # redis服务库
    username = redis_config['USERNAME']

    # 静态文件夹
    STATIC_FOLDER = '/static'
    # 取消ASCII编码
    JSON_AS_ASCII = False

    VERIFY_URL = []
