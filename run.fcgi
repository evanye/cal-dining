#!/home/e/ey/eye/ENV/bin/python
from flup.server.fcgi import WSGIServer
from api import app
WSGIServer(app).run()
