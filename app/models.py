from app import db

class Food(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True)
	dining_hall = db.Column(db.String(64), index = True)
	