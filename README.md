# 🏛️ eCourts Scraper

> **Automated Python tool to fetch case listings and cause lists from Indian eCourts.**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📖 Overview

**eCourts Scraper** is a Python-based project that automates fetching case information from  
[https://services.ecourts.gov.in](https://services.ecourts.gov.in).  

It allows users to:
- Search for cases by **CNR number** or by **Case Type + Case Number + Year**
- Check if the case is **listed today or tomorrow**
- Display the **serial number** and **court name**
- **Download case PDFs** (if available)
- **Download the entire cause list** for the day
- Save results as **JSON or text**

This project was created as part of an **Internship Task** focusing on data extraction and automation.

---

## 🧰 Tech Stack

| Tool / Library | Purpose |
|----------------|----------|
| **Python 3.10+** | Core programming language |
| **Requests** | HTTP client for fetching pages |
| **BeautifulSoup4** | HTML parsing |
| **Click** | Command-line interface |
| **Playwright** | Automated browser for captcha handling |
| **JSON / File I/O** | Data storage and saving |

---
## 📁 Project Structure

├── cli.py # CLI entrypoint
├── scraper.py # Main scraper logic
├── ecourts_client.py # HTTP + parsing
├── ecourts_playwright.py # Playwright browser automation
├── utils.py # Helpers (dates, file saving)
├── examples/
│ └── example_output.json
├── requirements.txt
└── README.md


---

## ⚙️ Installation & Setup

### 🧩 1️⃣ Clone the Repository
```bash
git clone https://github.com/Narayana276/ecourts_scraper.git
cd ecourts_scraper
#create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

#install dependencies
pip install -r requirements.txt
#(Optional) Install Playwright & Browsers
pip install playwright
playwright install
# or (alternative)
python -m playwright install

##🔍 Check Case by CNR Number for Today
python cli.py --cnr "MHBB010012342023" --today

##🔎 Check Case by Case Type, No, Year for Tomorrow
python cli.py --case-type "CR" --case-no 123 --case-year 2024 --tomorrow

##🧾 Download Today’s Cause List
python cli.py --causelist --out todays_causelist.json

##💾 Save Results to JSON File
python cli.py --cnr "MHBB010012342023" --today --out result.json

##🧩 Download Case PDF (if available)
python cli.py --cnr "MHBB010012342023" --today --download-pdf

#📜 License
This project is licensed under the MIT License — free to use, modify, and distribute for learning or research.

---

Would you like me to also include a **“Quick Start” one-liner section** at the top (for people who just want to clone and run in 3 commands)?  
Example:

```bash
git clone https://github.com/<user>/ecourts_scraper.git
cd ecourts_scraper
python cli.py --cnr "MHBB010012342023" --today




