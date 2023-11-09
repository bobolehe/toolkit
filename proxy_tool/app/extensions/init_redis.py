# 初始化redis
from flask_redis import FlaskRedis

redis_store = FlaskRedis()


def init_redis(app):
    redis_store.init_app(app)


