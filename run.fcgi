#!/home/e/ey/eye/.virtualenvs/flask/bin/python
from flup.server.fcgi import WSGIServer
from api import app

if __name__ == '__main__':
	WSGIServer(app).run()
