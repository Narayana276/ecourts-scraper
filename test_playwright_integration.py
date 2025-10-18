# test_playwright_integration.py
from ecourts_client import EcourtsClient
from ecourts_playwright import fetch_case_by_cnr_playwright

CNR_NUMBER = input("Enter CNR to test: ").strip()
html = fetch_case_by_cnr_playwright(CNR_NUMBER)
client = EcourtsClient()
parsed = client.parse_listing_html(html)
print("\n=== Parsed data ===")
print(parsed)
