from werkzeug.security import safe_str_compare
from user import User

users = [
    User(1, 'bob', 'asdf')
]

username__mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_compare(user.password, password):
        
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)