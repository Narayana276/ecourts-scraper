"""HTTP + HTML parsing logic for eCourts listings"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

SEARCH_URL_TEMPLATE = 'https://services.ecourts.gov.in/ecourtindia_v6/?p=case_status_cnr'

BASE_URL = 'https://services.ecourts.gov.in/ecourtindia_v6/'
HEADERS = {
    'User-Agent': 'eCourtsScraper/1.0 (+https://github.com/yourname)'
}


class EcourtsClient:
    def __init__(self, session=None):
        self.session = session or requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_page(self, url, params=None, method='GET'):
      try:
        if method == 'GET':
            r = self.session.get(url, params=params, timeout=15)
        else:
            r = self.session.post(url, data=params, timeout=15)
        r.raise_for_status()
        if "Invalid CNR Number" in r.text or "Case not found" in r.text:
            raise RuntimeError("Invalid or not found CNR.")
        return r.text
      except requests.RequestException as e:
        raise RuntimeError(f'Network error fetching {url}: {e}')


    def search_by_cnr(self, cnr):
      data = {'cnrno': cnr, 'submit': 'Search'}
      html = self.fetch_page(SEARCH_URL_TEMPLATE, params=data, method='POST')
      return html


    def search_by_components(self, case_type, number, year):
        params = {'caseType': case_type, 'caseNo': number, 'caseYear': year}
        return self.fetch_page(SEARCH_URL_TEMPLATE, params=params)

    def parse_listing_html(self, html, date_to_check=None):
        soup = BeautifulSoup(html, 'lxml')
        rows = []

        table = soup.find('table')
        if not table:
            for item in soup.select('.case-card, .cause-entry'):
                rows.append(self._parse_case_card(item))
            return rows

        for tr in table.find_all('tr'):
            cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if not cols or len(cols) < 2:
                continue
            serial = cols[0]
            court = cols[1]
            pdf_link = tr.find('a', href=re.compile(r'\\.pdf$'))
            pdf_url = urljoin(BASE_URL, pdf_link['href']) if pdf_link else None
            rows.append({
                'serial_no': serial,
                'court_name': court,
                'raw_cols': cols,
                'pdf_url': pdf_url,
            })
        return rows

    def _parse_case_card(self, node):
        serial = node.select_one('.serial, .sno')
        court = node.select_one('.court, .court-name')
        pdf = node.find('a', href=re.compile(r'\\.pdf$'))
        return {
            'serial_no': serial.get_text(strip=True) if serial else None,
            'court_name': court.get_text(strip=True) if court else None,
            'pdf_url': urljoin(BASE_URL, pdf['href']) if pdf else None,
        }

    def download_pdf(self, pdf_url, dest_folder='downloads'):
        os.makedirs(dest_folder, exist_ok=True)
        local_name = os.path.join(dest_folder, os.path.basename(pdf_url.split('?')[0]))
        try:
            r = self.session.get(pdf_url, stream=True, timeout=30)
            r.raise_for_status()
            with open(local_name, 'wb') as f:
                for chunk in r.iter_content(1024 * 32):
                    if chunk:
                        f.write(chunk)
            return local_name
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to download PDF {pdf_url}: {e}')
