from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import models

@app.route('/')
@app.route('/index')
def index():
	user = {'name': 'Evan'}
	return render_template("index.html", title = 'Home', user = user)