"""
ecourts_playwright.py
Automated browser method to fetch case info by CNR using Playwright.
"""

from playwright.sync_api import sync_playwright
import time

def fetch_case_by_cnr_playwright(cnr: str, wait_time: float = 6.0) -> str:
    """
    Opens the official eCourts website, searches for the given CNR,
    waits for results to load, and returns the page HTML.
    """
    url = "https://services.ecourts.gov.in/ecourtindia_v6/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True for silent mode
        page = browser.new_page()

        print("🌐 Opening eCourts website ...")
        page.goto(url, timeout=60000)

        # Click on "CNR Number" tab (wait if needed)
        page.click("text=CNR Number")
        time.sleep(2)

        # Fill CNR field
        print(f"🔍 Searching for CNR: {cnr}")
        page.fill("input#cnrno", cnr)

        # Manually solve captcha
        print("⚠️ Please solve the captcha in the browser window.")
        print("Waiting for you to submit the form ...")

        # Wait for user to press Enter after submitting manually
        input("➡️  After results load in browser, press ENTER here to continue...")

        # Grab full HTML after results appear
        html = page.content()

        # Save for debugging
        with open("debug_playwright_result.html", "w", encoding="utf-8") as f:
            f.write(html)

        browser.close()
        print("✅ Saved page HTML to debug_playwright_result.html")
        return html


if __name__ == "__main__":
    test_cnr = input("Enter CNR number: ").strip()
    fetch_case_by_cnr_playwright(test_cnr)
