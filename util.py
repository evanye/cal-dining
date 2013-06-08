from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

def http_get(url):
	resp = requests.get(url)
	return BeautifulSoup(resp.text, "lxml")

def get_date():
	return strip(datetime.now())

def get_recent_menu_date():
	date = datetime.now()
	if date.time().hour <= 3:
		return strip(date - timedelta(days=1))
	else:
		return strip(date)

def strip(date):
	return date.replace(hour = 0,  minute = 0, second = 0, microsecond = 0)