from flask import Flask
from concurrent.futures import ProcessPoolExecutor
from .init_redis import init_redis, redis_store


def init_plugs(app: Flask) -> None:
    init_redis(app)

