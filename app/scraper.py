from bs4 import BeautifulSoup
import requests
from datetime import datetime
from models import Food, Menu

BASE_URL = 'http://services.housing.berkeley.edu/FoodPro/dining/static/'
MENU_URL = 'todaysentrees.asp'
MEALS = {'breakfast':3, 'lunch': 5, 'dinner': 7}
DINING_COMMONS = {'crossroads':1, 'cafe3': 3, 'foothill': 5, 'clarkkerr': 7}
VEGE_LEGEND = {'vegan':'#800040', 'vegetarian':'#008000'}

def http_get(url):
	resp = requests.get(url)
	return BeautifulSoup(resp.text, "lxml")

def crawl():
	# make web request
	soup = http_get(BASE_URL + MENU_URL)

	# locate html data
	html = soup.body.contents[-1].table.tbody.contents[3].td.table.contents
	data = {}

	# extract data
	for MEAL in MEALS:
		meal_index = MEALS[MEAL]
		meal_data = html[meal_index]

		for DINING_COMMON in DINING_COMMONS:
			dc_index = DINING_COMMONS[DINING_COMMON]
			meal_dc_data = meal_data.contents[dc_index]

			for entry in meal_dc_data.find_all('a'):
				meal_name = entry.contents[0].string

				# skip the "Nutritive Analysis" link
				if 'nutritive analysis' in meal_name.lower():
					continue

				food_data = extract_food_info(entry)			

def extract_food_info(entry):
	link = BASE_URL + entry['href']
	meal_name = entry.contents[0].string
	gluten_free = False

	# truncate Honey Bear or Gluten Free prefix
	if meal_name[0:3] == 'HB ':
		meal_name = meal_name[3:]
	elif meal_name[0:3] == 'GF ':
		meal_name = meal_name[3:]
		gluten_free = True

	# check for vegan and vegetarian foods
	vegan, vegetarian = False, False
	if entry.font['color'] == VEGE_LEGEND['vegan']:
		vegan = True
	elif entry.font['color'] == VEGE_LEGEND['vegetarian']:
		vegetarian = True

	# crawl link (declared above) to check allergens
	allergens, ingredients = get_allergens_and_ingredients(link)

	return Food(name = meal_name, allergens = allergens, ingredients = ingredients, \
	vegan = vegan, vegetarian = vegetarian, gluten_free = gluten_free)

def get_allergens_and_ingredients(link):
	html = http_get(link)
	html = html.find_all(face="arial", size="2")[-2:]

	# edge case where no nutrition info is avaiable
	if len(html) <= 1:
		return "n/a", "n/a"

	allergens = html[0].contents[1].string if len(html[0].contents) > 1 else ""
	ingredients = html[1].contents[1].string if len(html[1].contents) > 1 else ""

	return allergens, ingredients

def get_date():
	return datetime.now().replace(hour = 0,  minute = 0, second = 0, microsecond = 0)