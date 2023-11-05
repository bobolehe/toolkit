from playwright.sync_api import Playwright, sync_playwright, expect

xpath_expression = '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody/tr/td/div'  # 替换为你的 XPath 表达式

def obtain_proxy(playwright: Playwright, proxy_list):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://geonode.com/free-proxy-list", timeout=60000)

    for i in range(5):
        # 等待指定 XPath 元素加载完成
        page.wait_for_selector(xpath_expression, state='attached')
        tr_elements = page.query_selector_all(
            '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody/tr')
        for tr in tr_elements:
            f = tr.query_selector('td')
            f2 = tr.query_selector('td:nth-child(2)')
            if f:
                ip = f.text_content()
                port = f2.text_content()
                proxy_list.append({'ip': ip, 'port': port})

        page.get_by_role("button", name="Next").click()
        # 等待指定 XPath 元素加载完成
        page.wait_for_selector(xpath_expression, state='attached')
    context.close()
    browser.close()


def run():
    proxy_list = []
    with sync_playwright() as playwright:
        obtain_proxy(playwright, proxy_list)
    return proxy_list


if __name__ == '__main__':
    proxy_list = run()
    print(proxy_list)
