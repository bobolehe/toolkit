import requests


def run():
    url = 'https://rootjazz.com/proxies/proxies.txt'
    r = requests.get(url)
    proxy_list = r.text.split('\n')

    ip_list = []

    for proxy in proxy_list:
        ip_port = proxy.split(':')
        if ip_port[0] != '':
            ip = ip_port[0]
            port = ip_port[1]
            ip_list.append({'ip': ip, 'port': port,'source': 'rootjazz'})

    return ip_list


if __name__ == '__main__':
    print(run())
