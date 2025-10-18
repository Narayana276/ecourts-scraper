"""
scraper.py — High-level orchestration for eCourts Scraper
"""
from datetime import date
from typing import Dict, Any, List
import logging

from ecourts_client import EcourtsClient
from utils import today_date, tomorrow_date, save_json, parse_date

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("scraper")


def _mark_date(entry: dict):
    """Try to detect a date string in entry text."""
    if entry.get("date"):
        return
    for field in ("raw_cols", "case_title", "raw_text"):
        val = entry.get(field)
        if not val:
            continue
        if isinstance(val, list):
            text = " ".join(val)
        else:
            text = str(val)
        d = parse_date(text)
        if d:
            entry["date"] = d
            return
    entry["date"] = None


def _filter_by_dates(entries: List[dict], dates: List[date]):
    out = []
    for e in entries:
        _mark_date(e)
        if e["date"] in dates or e["date"] is None:
            out.append(e)
    return out


def run_check(config: Dict[str, Any]) -> Dict[str, Any]:
    client = EcourtsClient()
    results = {"query": {}, "matches": [], "causelist": None, "errors": []}

    try:
        if config.get("cnr"):
          from ecourts_playwright import fetch_case_by_cnr_playwright
          html = fetch_case_by_cnr_playwright(config["cnr"])
        else:
          html = client.search_by_components(config["case_type"], config["case_no"], config["case_year"])

        matches = client.parse_listing_html(html)
    except Exception as e:
        results["errors"].append(str(e))
        return results

    # Filter by date
    filters = []
    if config.get("today"):
        filters.append(today_date())
    if config.get("tomorrow"):
        filters.append(tomorrow_date())

    if filters:
        results["matches"] = _filter_by_dates(matches, filters)
    else:
        results["matches"] = matches

    # Download PDFs
    if config.get("download_pdf"):
        for m in results["matches"]:
            if not m.get("pdf_url"):
                continue
            try:
                m["downloaded_path"] = client.download_pdf(m["pdf_url"])
            except Exception as e:
                m["download_error"] = str(e)

    # Console output
    for m in results["matches"]:
        print("---")
        print(f"Serial: {m.get('serial_no')}")
        print(f"Court : {m.get('court_name')}")
        if m.get('pdf_url'):
            print(f"PDF   : {m.get('pdf_url')}")
        if m.get('downloaded_path'):
            print(f"Saved : {m.get('downloaded_path')}")

    return results
