import json
import redis
from redis_tool import config as setting

from log import log_data


class RedisProxy:

    def __init__(self):
        host = setting.redis_config["HOST"]  # redis服务地址
        port = setting.redis_config["PORT"]  # redis服务端口
        password = setting.redis_config["PASSWORD"]  # redis服务密码
        db = setting.redis_config["DB"]  # redis服务库
        username = setting.redis_config['']

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
            # data = self.ret.get(key)
        except Exception as e:
            log_data.error(f'成功代理存储redis失败，错误信息{e}')
        else:
            log_data.info(f"测试成功代理存储redis成功")

    def w_hset(self, data, key, hset_name):
        try:
            for x in data:
                hsname = x['name']
                self.ret.hset(hset_name, hsname, str(x))
        except Exception as e:
            log_data.error(f'成功代理存储redis失败，错误信息{e}')
        else:
            log_data.info(f"测试成功代理存储redis成功")

    def r_json(self, key):
        data = self.ret.get(key)
        # data = json.loads(data)
        return data

    def r_hgetall(self, key):
        data = self.ret.hgetall(key)
        print(type(data))
        return data


if __name__ == '__main__':
    re = RedisProxy()
    data = re.r_hgetall(key="use_proxy")
    for d in data:
        print(d)
    # print(re.w(data='test', key="proxy_list"))
