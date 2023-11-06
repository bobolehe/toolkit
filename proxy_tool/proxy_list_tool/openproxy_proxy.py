from playwright.sync_api import Playwright, sync_playwright, expect

xpath_expression = '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody/tr/td/div'  # 替换为你的 XPath 表达式


def obtain_proxy(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://openproxy.space/list/http")
    page.wait_for_selector('//*[@id="root"]/div[2]/div[1]/section[4]/textarea', state='attached')
    proxy_text = page.query_selector('//*[@id="root"]/div[2]/div[1]/section[4]/textarea').inner_html()
    proxy_list = proxy_text.split('\r\n')
    proxy_list = [{'ip': proxy.split(':')[0], 'port': proxy.split(':')[1]} for proxy in proxy_list]
    # ---------------------
    context.close()
    browser.close()
    return proxy_list


def run():
    with sync_playwright() as playwright:
        proxy_list = obtain_proxy(playwright)
    return proxy_list


if __name__ == '__main__':
    proxy_list = run()
    print(proxy_list)
