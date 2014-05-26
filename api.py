from flask import Flask, render_template, make_response, request, jsonify, current_app
from flask.ext.restful import abort, Api
from flask.ext.sqlalchemy import SQLAlchemy
from functools import update_wrapper

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

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
    headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
    origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    if methods is not None:
      return methods

    options_resp = current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f):
    def wrapped_function(*args, **kwargs):
      if automatic_options and request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()
      else:
        resp = make_response(f(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
        return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

      f.provide_automatic_options = False
    return update_wrapper(wrapped_function, f)
  return decorator

@app.route('/menu', methods = ['GET'])
@crossdomain(origin='*')
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

