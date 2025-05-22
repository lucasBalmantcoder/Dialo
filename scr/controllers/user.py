
from flask import Blueprint, jsonify, request
from sqlalchemy import inspect

from scr.controllers.models.models import User
from scr.db import db
from http import HTTPStatus
from werkzeug.security import generate_password_hash

# lovalhost:5000/users/
app = Blueprint('users', __name__, url_prefix='/users')

GET =  "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"

def _create_user():
    data = request.json
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return {"error": "Missing required fields"}, HTTPStatus.BAD_REQUEST
    
    errors = {}
    
    if User.query.filter_by(username=data["username"]).first():
        errors["username"] = "Username already exists"
    
    if User.query.filter_by(email=data["email"]).first():
        errors["email"] = "Email already exists"
    
    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    hashed_password = generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        email=data["email"],
        password_with_hash=hashed_password
    )
    # db.session.add(user)
    # db.session.commit()
    
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    # ✅ RESPOSTA explícita ao final:
    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, HTTPStatus.CREATED



    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()   
    
    return [ 
            
    {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "hashed_password": user.password_with_hash
    }
    for user in users
    
]





@app.route('/', methods=[GET, POST])
def handler_user():
    if request.method == POST:
        return _create_user()
        return {'message': 'user created!'}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()} 
    
    
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
            
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.password_with_hash
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

@app.route('/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT