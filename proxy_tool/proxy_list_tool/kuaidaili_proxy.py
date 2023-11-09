import time

from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime


def obtain_proxy(playwright: Playwright, proxy_list: list, urls: list):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    for url in urls:
        try:
            page.goto(url)
            # with open('测试页.html', 'w', encoding='utf-8') as f:
            #     f.write(page.content())
            # 使用Beautiful Soup解析HTML
            soup = BeautifulSoup(page.content(), 'html.parser')
            # 使用Beautiful Soup进行查找

            elements = soup.select('#list div table tbody tr')
            for tr in elements:
                ip = tr.select('td')[0].text
                port = tr.select('td')[1].text
                proxy_list.append({'ip': ip, 'port': port,'source': 'kuaidaili'})
        except Exception as e:
            continue

    context.close()
    browser.close()


def run():
    url = 'https://www.kuaidaili.com/free/'
    urls = 'https://www.kuaidaili.com/free/inha/%s/'
    url_list = [urls % i for i in range(2, 10)]
    url_list.append(url)
    proxy_list = []
    with sync_playwright() as playwright:
        obtain_proxy(playwright, proxy_list, url_list)
    return proxy_list


if __name__ == '__main__':
    proxy_list = run()
    if not proxy_list:
        proxy_list = run()
    print(proxy_list)
