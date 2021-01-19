from flask import request, Response, g, current_app
from functools import wraps
import config
import jwt
from model import UserDao

def login_required(f):      
    @wraps(f)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization') 
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms=current_app.config['JWT_ALGORITHM']) 
            except jwt.InvalidTokenError:
                 payload = None     

            if payload is None: return Response(status=401)  

            user_id   = payload['id']  
            g.user_id = user_id
        else:
            return Response(status = 401)  

        return f(*args, **kwargs)
    return decorated_function

