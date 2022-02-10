# from flask_httpauth import HTTPBasicAuth
from RestApiImplementation.models_api import User
from RestApiImplementation.schemas import UserSchema
from RestApiImplementation.models_api import Session

from flask import request
from flask import Blueprint
from RestApiImplementation.au import verify_password
from RestApiImplementation.au import auth
import bcrypt

session = Session()

user = Blueprint("user",__name__)

from RestApiImplementation.utils_db import (
    create_entry,
    get_entries,
    get_entry_by_id,
    update_entry_by_id,
    delete_entry_by_id,
)


user = Blueprint("user",__name__)
@user.route("/user", methods=["POST"])  # create new user
def create_user():
    user_data = UserSchema().load(request.get_json())
    pos = request.json.get('position',None)
    pwd = request.json.get('password', None)
    hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    user_data.update({"password": hashed_pwd})
    temp = create_entry(User, UserSchema, **user_data)
    return temp


@user.route("/user", methods=["GET"])  # get all users
def get_user():
    return get_entries(User, UserSchema)


@user.route("/user/<int:id>", methods=["GET"])  # get user by id
def get_user_by_id(id):
    return get_entry_by_id(User, UserSchema, id)


@user.route("/user", methods=["PUT"])  # update user by id
@auth.login_required()
def update_user_by_id():
    user = session.query(User).filter_by(email = auth.current_user()).first()
    user_data = UserSchema().load(request.get_json())
    templist = list(user_data)
    if 'password' in templist:
        pwd = request.json.get('password', None)
        hashed_pwd = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
        user_data.update({"password": hashed_pwd})
    return update_entry_by_id(User, UserSchema, user.id, **user_data)


@user.route("/user", methods=["DELETE"])  # delete user by id
@auth.login_required
def delete_user_by_id():
    user = session.query(User).filter_by(email = auth.current_user()).first()
    return delete_entry_by_id(User, UserSchema, user.id)