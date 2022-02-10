
from RestApiImplementation.models_api import JoinRequest
from RestApiImplementation.models_api import User
from RestApiImplementation.models_api import Session
from RestApiImplementation.schemas import JoinRequestSchema
from flask import Blueprint
from flask import Response
# from flask_httpauth import HTTPBasicAuth
from flask import request
from RestApiImplementation.au import verify_password,auth
from RestApiImplementation.utils_db import InvalidUsage

from RestApiImplementation.utils_db import (
    create_entry,
    update_entry_by_id
)
session = Session()
join = Blueprint("join", __name__)
# auth = HTTPBasicAuth()
@join.route("/joinrequest", methods=["POST"])  # create new auditorium
def create_joinrequest():
    JoinRequestData = JoinRequestSchema().load(request.get_json())
    templ = list(JoinRequestData)
    if 'access' in templ:
        raise InvalidUsage("You are not allowed to set access", status_code=400)
    user = session.query(User).filter_by(id=request.json.get('studentID')).first()
    return create_entry(JoinRequest, JoinRequestSchema, **JoinRequestData)



@join.route("/joinrequest/<int:id>", methods=["PUT"])  # update auditorium by id
def update_auditorium_by_id(id):
        JoinRequestData = JoinRequestSchema().load()
        templ = list(JoinRequestData)
        return update_entry_by_id(JoinRequest, JoinRequestSchema, id, **JoinRequestData)