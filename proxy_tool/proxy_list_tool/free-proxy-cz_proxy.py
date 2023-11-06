from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://free-proxy.cz/en/proxylist/country/all/http/ping/all/5")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)