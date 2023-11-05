import requests
import base64

url = 'https://proxylist.geonode.com/api/organdasn?limit=100&page=4'
import time

from playwright.sync_api import sync_playwright
url = 'https://geonode.com/free-proxy-list'
xpath_expression = '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody/tr/td/div'  # 替换为你的 XPath 表达式

with sync_playwright() as p:
    # 指定为有头模式，Ture为无头模式
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)
    # 等待指定 XPath 元素加载完成
    page.wait_for_selector(xpath_expression, state='attached')
    print(page.inner_html(
        '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody'))
    browser.close()

if __name__ == '__main__':
    pass
