import datetime
import requests
import threading

from functools import partial
from log import log_data
from concurrent.futures import ThreadPoolExecutor
from ..check_proxy.redis_tool import RedisProxy

yes_proxy_list = []

rds = RedisProxy()
url = 'https://www.rapid7.com/db/modules/post/linux/gather/enum_nagios_xi/'


def check_proxy(proxy, url):
    # 设置代理参数
    proxies = {
        'http': f'http://{proxy["ip"]}:{proxy["port"]}',
        'https': f'https://{proxy["ip"]}:{proxy["port"]}',
    }

    try:
        # 发送请求，指定代理参数
        response = requests.get(url, proxies=proxies)
        # 检查响应状态码
        if response.status_code == 200:
            yes_proxy_list.append(proxy)
            rds.w_h(data=yes_proxy_list, key=f'{url}')
    except requests.exceptions.RequestException as e:
        pass


def run_check(url):
    proxy_list = rds.r_h('primary_proxy')
    log_data.info(f"需要验证数据量{len(proxy_list)}")
    rds.ret.delete(url)
    max_threads = 100  # 假设最大线程数量为100
    with ThreadPoolExecutor(max_threads) as executor:
        check_proxy_partial = partial(check_proxy, url=url)
        valid_proxies = list(executor.map(check_proxy_partial, proxy_list))


if __name__ == '__main__':
    run_check(url)
