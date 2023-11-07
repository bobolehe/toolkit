import requests
from concurrent.futures import ThreadPoolExecutor
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

yes_proxy_list = []


def query_proxy():
    proxy_list = []
    proxy_list += crun()
    # proxy_list += grun()
    # proxy_list += krun()
    # proxy_list += krun2()
    # proxy_list += orun()
    # proxy_list += srun()
    # proxy_list += rrun()
    # proxy_list += prun()

    return proxy_list


def check_proxy(proxy):
    # for proxy in proxys:
    url = 'https://www.rapid7.com/db/modules/payload/windows/dllinject/bind_tcp_rc4/'
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
            print(yes_proxy_list)
            yes_proxy_list.append(proxy)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


if __name__ == '__main__':
    proxy_list = query_proxy()
    # check_proxy(proxy_list, url='https://www.rapid7.com/db/modules/payload/windows/dllinject/bind_tcp_rc4/')
    # 使用线程池来并行测试代理
    url = 'https://www.rapid7.com/db/modules/payload/windows/dllinject/bind_tcp_rc4/'
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(check_proxy, proxy_list)
    print(yes_proxy_list)
