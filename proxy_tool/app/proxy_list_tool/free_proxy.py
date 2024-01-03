from playwright.sync_api import Playwright, sync_playwright, expect


def obtain_proxy(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://free-proxy-list.net/")
    proxy_list = []
    tr_list = page.query_selector_all('//*[@id="list"]/div/div[2]/div/table/tbody/tr')
    for tr in tr_list:
        ip = tr.query_selector('td:nth-child(1)').inner_text()
        port = tr.query_selector('td:nth-child(2)').inner_text()
        proxy_list.append({'ip': ip, 'port': port,'source': 'free_proxy'})
    context.close()
    browser.close()
    return proxy_list


def run():
    with sync_playwright() as playwright:
        proxy_list = obtain_proxy(playwright)
    return proxy_list


if __name__ == '__main__':
    run()
