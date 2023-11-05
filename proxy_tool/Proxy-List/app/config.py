import setting
from urllib.parse import quote_plus as urlquote


class BaseConfig:
    SECRET_KEY = "pear-admin-flask"
    # JWT密钥
    JWT_SECRET_KEY = 'JwTOn1'
    # JWT有效期 通过redis进行管理则无需设置管理时间
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    # redis配置
    host = setting.redis_config["HOST"]  # redis服务地址
    port = setting.redis_config["PORT"]  # redis服务端口
    password = setting.redis_config["PASSWORD"]  # redis服务密码
    db = setting.redis_config["DB"]  # redis服务库

    REDIS_URL = f'redis://:{password}@{host}:{port}/{db}'
    REDIS_PASSWORD = password

    # 静态文件夹
    STATIC_FOLDER = '/static'
    # 取消ASCII编码
    JSON_AS_ASCII = False
