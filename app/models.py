from app import db

class Food(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	allergens = db.Column(db.String(512))
	ingredients = db.Column(db.String(2048))
	vegan = db.Column(db.Boolean(), index = True)
	vegetarian = db.Column(db.Boolean(), index = True)
	gluten_free = db.Column(db.Boolean())

	def __repr__(self):
		return "Food: {0}, vegan: {1}, vegetarian: {2}, GF: {3}, \
		allergens: {4}, ingredients: {5}".format(self.name, \
		self.vegan, self.vegetarian, self.gluten_free, self.allergens, self.ingredients)

MEAL_TO_ENUM = {'breakfast': 1, 'lunch': 2, 'dinner': 3}
ENUM_TO_MEAL = {1: 'breakfast', 2: 'lunch', 3: 'dinner'}

class Menu(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date = db.Column(db.Date, index = True)
	location = db.Column(db.String(64), index = True)
	meal = db.Column(db.Integer, index = True)
	food = db.Column(db.Integer, db.ForeignKey('food.id'))

	def __repr__(self):
		return "Date: {0}, Located: {1}, Meal: {2}, Food: {3}".format(date, location, meal, food)
	