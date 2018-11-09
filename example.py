# app.py
#import psutil
import os
from functools import wraps
from flask import Flask, request, Response
app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

ospid = os.getpid()
#p = psutil.Process()
#c = p.cpu_percent()
#m = p.virtual_memory()	
	
@app.route("/")
@requires_auth  #requires_auth decorator for basic auth
def hello():
   return 'PID of current app: ', ospid

if __name__ == '__main__':
    app.run()
