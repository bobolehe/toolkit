import time

from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime


def obtain_proxy(playwright: Playwright, proxy_list: list, url: str):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url, timeout=60000)

    with open('测试页.html', 'w', encoding='utf-8') as f:
        f.write(page.content())

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(page.content(), 'html.parser')
    #
    # 使用Beautiful Soup进行查找
    elements = soup.select('#list div table tbody tr')
    for tr in elements:
        ip = tr.select('td')[0].text
        port = tr.select('td')[1].text
        proxy_list.append({'ip': ip, 'port': port})
    context.close()
    browser.close()


def run():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化为字符串，例如：2023-10-06
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    url = 'https://www.kuaidaili.com/free/'
    proxy_list = []
    with sync_playwright() as playwright:
        obtain_proxy(playwright, proxy_list, url)
    return proxy_list


if __name__ == '__main__':
    proxy_list = run()
    if not proxy_list:
        proxy_list = run()
    print(proxy_list)
