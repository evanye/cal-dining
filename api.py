from flask import Flask, render_template
from flask.ext.restful import abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)

from models import Menu, Food, menu_to_json
from util import get_recent_menu_date

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

class DiningMenu(Resource):
	def get(self, date = get_recent_menu_date().strftime("%Y-%m-%d")):
		menu = menu_to_json(date)
		if len(menu) > 0:
			return menu
		else:
			abort(404, message='No menus for {0}'.format(date))

class FoodInfo(Resource):
	def get(self, food):
		food_info = food

api.add_resource(DiningMenu, '/menu/')
api.add_resource(DiningMenu, '/menu/<string:date>')