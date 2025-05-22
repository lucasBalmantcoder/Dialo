from flask import Blueprint, request
from sqlalchemy import inspect

from scr.controllers.models.models import User
from scr.db import db
from http import HTTPStatus


# lovalhost:5000/users/
app = Blueprint('user', __name__, url_prefix='/users')

GET =  "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"


def _create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user )
    db.session.commit()
    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()   
    
    return [ 
            
    {
        "id": user.id,
        "username": user.username,
    }
    for user in users
    
]
    
    

@app.route('/', methods=[GET, POST])
def handler_user():
    if request.method == POST:
        _create_user()
        return {'message': 'user created!'}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()} 
    
    
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
            
            "id": user.id,
            "username": user.username,
        }
        
@app.route('/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id) 
    data = request.json

    # if not data or "username" not in data:
    #     return {"error": "Missing 'username'"}, HTTPStatus.BAD_REQUEST
    
    # user.username = data["username"]
    # db.session.commit()
    mapper = inspect(User)
    for column in mapper.columns:
        if column.name in data:
            setattr(user, column.name, data[column.name])
    db.session.commit()
    

    return {
        "id": user.id,
        "username": user.username,
    }, HTTPStatus.OK

@app.route('/<int:user_id>')
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT