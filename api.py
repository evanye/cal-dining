from flask import Flask, render_template
from flask.ext.restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)


from models import Menu, Food, menuToJson
from util import get_recent_menu_date

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

class DiningMenu(Resource):
	def get(self, date = get_recent_menu_date().strftime("%Y-%m-%d")):
		print date
		menu = menuToJson(date)
		if len(menu) > 0:
			return menu
		else:
			abort(404, message='No menus for {0}'.format(date))

# api.add_resource(DiningMenu, '/menu')
api.add_resource(DiningMenu, '/menu/<string:date>')
		


