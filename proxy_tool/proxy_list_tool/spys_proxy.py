from playwright.sync_api import Playwright, sync_playwright, expect

xpath_expression = '//*[@id="__next"]/div/div/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div/table/tbody/tr/td/div'  # 替换为你的 XPath 表达式


def obtain_proxy(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://spys.one/en/http-proxy-list/")
    page.locator("#xpp").select_option("5")
    try:
        page.wait_for_selector('//table[2]/tbody/tr[4]/td/table/tbody/tr[500]', state='attached')
    except Exception as e:
        page.locator("#xpp").select_option("5")

    tr_list = page.query_selector_all('//table[2]/tbody/tr[4]/td/table/tbody/tr')[2:-1]
    proxy_list = []
    for tr in tr_list:
        td = tr.query_selector('td')
        ip, port = td.inner_text().split(':')
        proxy_list.append({'ip': ip, 'port': port})

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
