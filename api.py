from flask import Flask, render_template, request, jsonify
from flask.ext.restful import abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)

from models import Menu, Food
from util import get_recent_menu_date, menu_to_json

@app.route('/')
@app.route('/index.html')
def index():
  return render_template("index.html")

@app.route('/menu', methods = ['GET'])
def get_menu():
  if request.method == 'GET':
    params = {
      'date': request.args.get('date', get_recent_menu_date().strftime("%Y-%m-%d")),
      'meal': request.args.getlist('meal'),
      'location': request.args.getlist('location'),
      'start_date': request.args.get('start', None),
      'end_date': request.args.get('end', None)
    }

    if len(params['meal']) == 0:
      params['meal'] =  ['breakfast', 'lunch', 'dinner']
    if len(params['location']) == 0:
      params['location'] =  ['crossroads', 'cafe3', 'foothill', 'clarkkerr']

    try:
      return jsonify(menu_to_json(params))
    except Exception:
      abort(400, message='Sorry, your request could not be parsed. Check your params again for typos!')