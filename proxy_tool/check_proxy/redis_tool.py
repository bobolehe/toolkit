import json
import redis
from ..check_proxy import config as setting
from ...log import log_data


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
        except Exception as e:
            log_data.error(f'存储redis失败，错误信息{e}')
        else:
            log_data.info(f"存储redis成功")

    def r(self, key):
        data = self.ret.get(key)
        data = json.loads(data)
        return data['success']

    def w_h(self, data, key):
        try:
            for x in data:
                hsname = x['ip']
                x = json.dumps(x)
                self.ret.hset(key, hsname, x)
        except Exception as e:
            log_data.error(f'存储redis失败，错误信息{e}')
        else:
            log_data.info(f"存储redis成功")

    def r_h(self, key):
        r_list = self.ret.hgetall(key)
        data_list = []
        for d in r_list:
            temp = json.loads(self.ret.hget(key, d).decode('utf-8'))
            data_dict = {d.decode('utf-8'): temp}
            data_list.append(temp)
        return data_list


if __name__ == '__main__':
    re = RedisProxy()
    # data = re.r_h(key="use_proxy")
    data = re.ret.hget('primary_proxy', '218*')
    print(data)
    # if data:
    #     re.ret.hdel('primary_proxy', '36.134.91.82')
