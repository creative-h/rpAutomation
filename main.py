from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto("http://185.131.55.105:8058/Login")

    print(page.title())

    input("Press Enter...")

    browser.close()