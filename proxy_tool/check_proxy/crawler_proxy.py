import datetime

from proxy_tool.proxy_list_tool.checkerproxy_proxy import run as crun
from proxy_tool.proxy_list_tool.english_proxy import run as erun  # 需要代理
from proxy_tool.proxy_list_tool.free_proxy import run as frun
from proxy_tool.proxy_list_tool.geonode_proxy import run as grun
from proxy_tool.proxy_list_tool.kuaidaili_proxy import run as krun
from proxy_tool.proxy_list_tool.kuaidaili2_proxy import run as krun2
from proxy_tool.proxy_list_tool.openproxy_proxy import run as orun
from proxy_tool.proxy_list_tool.spys_proxy import run as srun
from proxy_tool.proxy_list_tool.rootjazz_proxy import run as rrun
from proxy_tool.proxy_list_tool.proxyspace_proxy import run as prun
from proxy_tool.proxy_list_tool.proxylistplus_proxy import run as pprun

from proxy_tool.check_proxy.redis_tool import RedisProxy

yes_proxy_list = []

rds = RedisProxy()


def query_proxy():
    proxy_list = []
    # rds.ret.delete('primary_proxy')

    proxy_list += crun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += grun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += krun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += krun2()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += orun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += srun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += rrun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    proxy_list += prun()
    rds.w_h(data=proxy_list, key='primary_proxy')

    return proxy_list


if __name__ == '__main__':
    proxy_list = query_proxy()
