from bs4 import BeautifulSoup
import requests
from datetime import datetime
from api import db
from models import Food, Menu, LOCATION_TO_ENUM, MEAL_TO_ENUM

BASE_URL = 'http://services.housing.berkeley.edu/FoodPro/dining/static/'
MENU_URL = 'todaysentrees.asp'
MEALS = {'breakfast':3, 'lunch': 5, 'dinner': 7}
DINING_COMMONS = {'crossroads':1, 'cafe3': 3, 'foothill': 5, 'clarkkerr': 7}
VEGE_LEGEND = {'vegan':'#800040', 'vegetarian':'#008000'}

def crawl():
	# make web request
	soup = http_get(BASE_URL + MENU_URL)
	# locate html data
	html = soup.body.contents[-1].table.tbody.contents[3].td.table.contents

	# stores food that has already been added to the table
	food_cache = {}

	# extract data
	for MEAL in MEALS:
		meal_index = MEALS[MEAL]
		meal_data = html[meal_index]

		for DINING_COMMON in DINING_COMMONS:
			dc_index = DINING_COMMONS[DINING_COMMON]
			meal_dc_data = meal_data.contents[dc_index]

			for entry in meal_dc_data.find_all('a'):
				meal_name = entry.contents[0].string
				meal_name, gluten_free = truncate_meal_name(meal_name)

				# skip the "Nutritive Analysis" link
				if 'nutritive analysis' in meal_name.lower():
					continue

				# create database models object
				if meal_name in food_cache:	 
					food_obj = food_cache[meal_name]
				else: # food is not located in local cache
					  # check if food is in database
					food_obj = Food.query.filter_by(name=meal_name).first()
					  # not found in database, crawl page
					if food_obj is None:
						food_obj = extract_food_info(entry)
						db.session.add(food_obj)

					  # add food to the cache
					food_cache[meal_name] = food_obj

				menu_obj = Menu(date = get_date(), location = LOCATION_TO_ENUM[DINING_COMMON], \
				meal = MEAL_TO_ENUM[MEAL], food = food_obj)

				db.session.add(menu_obj)
	db.session.commit()

def extract_food_info(entry):
	link = BASE_URL + entry['href']
	meal_name = entry.contents[0].string
	meal_name, gluten_free = truncate_meal_name(meal_name)

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

# truncate Honey Bear or Gluten Free prefix
# 	returns pair of meal name, and if its gluten free or not
def truncate_meal_name(meal_name):
	gluten_free = False
	if meal_name[0:3] == 'HB ':
		meal_name = meal_name[3:]
	elif meal_name[0:3] == 'GF ':
		meal_name = meal_name[3:]
		gluten_free = True
	return meal_name, gluten_free

def http_get(url):
	resp = requests.get(url)
	return BeautifulSoup(resp.text, "lxml")

def get_date():
	return datetime.now().replace(hour = 0,  minute = 0, second = 0, microsecond = 0)