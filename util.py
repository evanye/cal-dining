from bs4 import BeautifulSoup
import requests
from sqlalchemy import and_
from datetime import date, datetime, timedelta
from models import Menu, Food, LOCATION_TO_ENUM, ENUM_TO_LOCATION, MEAL_TO_ENUM, ENUM_TO_MEAL

def http_get(url):
  resp = requests.get(url)
  return BeautifulSoup(resp.text, "lxml")

def get_date():
  now = datetime.now()
  return date(now.year, now.month, now.day)

def get_recent_menu_date():
  now = datetime.now()
  if now.time().hour <= 3:
    now -= timedelta(days = 1)
  return date(now.year, now.month, now.day)

def date_from_string(str):
  date_obj = datetime.strptime(str, "%Y-%m-%d")
  return date(date_obj.year, date_obj.month, date_obj.day)

def menu_to_json(params):
  from datetime import date
  json = {}
  if params['start_date'] is not None:
    start = max(date_from_string(params['start_date']), date(2013,6,1))
    end = get_date()
    if params['end_date'] is not None:
      end = min(date_from_string(params['end_date']), end)

    dates = [start + timedelta(n) for n in range((end-start).days)]
  else:
    dates = [date_from_string(params['date'])]
  
  for date in dates:
    date_string = date.strftime("%Y-%m-%d")
    json[date_string] = {}
    for meal in params['meal']:
      json[date_string][meal] = {}
      for location in params['location']:
        json[date_string][meal][location] = {}

  query = Menu.query
  if 'start' in locals():
    query = query.filter(and_(Menu.date >= start, Menu.date <= end))
  else:
    query = query.filter_by(date = params['date'])

  query = query.filter(Menu.meal.in_([MEAL_TO_ENUM[meal] for meal in params['meal']]))
  query = query.filter(Menu.location.in_([LOCATION_TO_ENUM[location] for location in params['location']]))

  # lazy way of handling n+1 joins, works until Food gets super large
  all_food = Food.query.all()
  for entry in query.all():
    food = all_food[entry.food_id - 1]
    date = entry.date.strftime("%Y-%m-%d")
    location = ENUM_TO_LOCATION[int(entry.location)]
    meal = ENUM_TO_MEAL[int(entry.meal)]
    food_info = {'allergens': food.allergens, 'ingredients': food.ingredients, \
            'vegan': food.vegan, 'vegetarian': food.vegetarian}
    json[date][meal][location][food.name] = food_info
  return flatten(json)

def flatten(obj):
  if isinstance(obj, dict):
    for key in obj:
      obj[key] = flatten(obj[key])

    if len(obj) == 1:
      for key in obj:
        obj = obj[key]
        break
  return obj
