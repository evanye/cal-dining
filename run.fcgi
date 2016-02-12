#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from api import app
WSGIServer(app).run()
