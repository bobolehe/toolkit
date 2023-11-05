import json
import redis
import setting

from loggingtool import logger



class RedisProxy:

    def __init__(self):
        host = setting.redis_config["HOST"]  # redis服务地址
        port = setting.redis_config["PORT"]  # redis服务端口
        password = setting.redis_config["PASSWORD"]  # redis服务密码
        db = setting.redis_config["DB"]  # redis服务库

        if password:
            self.ret = redis.StrictRedis(host=host, port=port, password=password, db=db)
        else:
            self.ret = redis.StrictRedis(host=host, port=port, db=db)

    def w(self, data, key):
        try:
            # 设置键值
            test = json.dumps(data)
            self.ret.set(key, test)
            # 获取指定键值
            data = self.ret.get(key)
        except Exception as e:
            logger.error(f'成功代理存储redis失败，错误信息{e}')
        else:
            logger.info(f"测试成功代理存储redis成功")

    def r(self, key):
        data = self.ret.get(key)
        data = json.loads(data)
        return data['success']


if __name__ == '__main__':
    re = RedisProxy()
    print(re.r(key="proxy_list"))
