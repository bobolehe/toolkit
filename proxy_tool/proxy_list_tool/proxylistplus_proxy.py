import requests
from bs4 import BeautifulSoup


def obtain_proxy(urls):
    proxy_list = []
    for url in urls:
        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')
        # 使用Beautiful Soup进行查找

        elements = soup.select('#page table')
        elements = elements[2].select('tr')
        for tr in elements[2:]:
            ip = tr.select('td')[1].text
            port = tr.select('td')[2].text
            proxy_list.append({'ip': ip, 'port': port})
    print(proxy_list)
    return proxy_list


def run():
    url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s'
    urls = [url % i for i in range(1, 5)]
    return obtain_proxy(urls)
