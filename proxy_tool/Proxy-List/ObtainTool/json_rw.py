import json
from loggingtool import logger
import setting
import os
from ObtainTool import RedisProxy


json_file = setting.JSON_FILE


def w(data, redis_key):
    if setting.js_switch:
        with open(json_file, "w") as f:
            json.dump(data, f)
        logger.info("写入文件完成...")

    if setting.redis_switch:
        RedisProxy.w(data=data, key=redis_key)


def r():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            logger.info(type(data['one']))
            logger.info(type(data))
    else:
        pass
