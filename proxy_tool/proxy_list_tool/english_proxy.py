from playwright.sync_api import Playwright, sync_playwright, expect


def obtain_proxy(playwright: Playwright, urls):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    proxy_list = []
    for url in urls:
        print(url)
        page.goto(url)
        ul_list = page.query_selector_all('//*[@id="proxy-table"]/div[2]/div/ul')
        for ul in ul_list:
            li = ul.query_selector('li')
            ip, port = li.inner_text().split(':')
            proxy_list.append({'ip': ip, 'port': port})
    context.close()
    browser.close()
    return proxy_list


def run():
    url = "https://proxy-list.org/english/index.php?p=%s"
    urls = [url % i for i in range(1, 11)]
    with sync_playwright() as playwright:
        proxy_list = obtain_proxy(playwright, urls)
    print(proxy_list)
    return proxy_list


if __name__ == '__main__':
    run()
