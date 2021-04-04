from __init__ import app
from env import PORT_env, HOST_env
DEBUG = True
PORT = PORT_env
HOST = HOST_env

app.run(debug=DEBUG, host=HOST, port=PORT)
