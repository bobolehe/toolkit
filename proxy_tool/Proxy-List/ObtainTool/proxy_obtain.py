import random
from loggingtool import logger
from ObtainTool import RedisProxy


class ProxyObtain:

    def get_proxy(self):
        proxy_list = RedisProxy.r(key="success_proxy")
        return random.choice(proxy_list)

    def all_proxy(self):
        proxy_list = RedisProxy.r(key="success_proxy")
        return proxy_list


if __name__ == '__main__':
    pass
