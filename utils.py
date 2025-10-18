"""Utility helpers for eCourts scraper"""
from datetime import datetime, timedelta
import json
import os
from dateutil import parser


def today_date():
    return datetime.now().date()


def tomorrow_date():
    return (datetime.now() + timedelta(days=1)).date()


def parse_date(text):
    try:
        return parser.parse(text).date()
    except Exception:
        return None


def save_json(obj, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
