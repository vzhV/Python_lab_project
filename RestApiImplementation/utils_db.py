from RestApiImplementation.models_api import Session, JoinRequest, User
from flask import jsonify
from flask_bcrypt import check_password_hash, Bcrypt
from functools import wraps
from RestApiImplementation.schemas import JoinRequestSchema

session = Session()
bcrypt = Bcrypt()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

def db_lifecycle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ValueError):
                return jsonify({'message': e.args[0], 'type': 'ValueError'}), 400
            elif isinstance(e, AttributeError):
                return jsonify({'message': e.args[0], 'type': 'AttributeError'}), 400
            elif isinstance(e, KeyError):
                return jsonify({'message': e.args[0], 'type': 'KeyError'}), 400
            elif isinstance(e, TypeError):
                return jsonify({'message': e.args[0], 'type': 'TypeError'}), 400
            else:
                raise e

    return wrapper


def session_lifecycle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rez = func(*args, **kwargs)
            session.commit()
            return rez
        except Exception as e:
            session.rollback()
            raise e

    return wrapper


@db_lifecycle
@session_lifecycle
def create_entry(model_class, model_schema, **kwargs):  # POST entity
    entry = model_class(**kwargs)
    session.add(entry)
    return jsonify(model_schema().dump(entry))



@db_lifecycle
def get_entries(model_class, model_schema):  # GET all entries
    entries = session.query(model_class).all()
    return jsonify(model_schema(many=True).dump(entries))

@db_lifecycle
def get_entry_by_id(model_class, model_schema, id):  # GET entry by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    return jsonify(model_schema().dump(entry))

@db_lifecycle
@session_lifecycle
def get_course_by_id(id, userID):  # GET entry by id
    entry = session.query(JoinRequest).filter_by(studentID=userID, courseID=id).first()
    if entry is None:
        raise InvalidUsage("No access", status_code=401)
    return jsonify(JoinRequestSchema().dump(entry))

@db_lifecycle
@session_lifecycle
def update_entry_by_id(model_class, model_schema, id, **kwargs):  # PUT entity by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    for key, value in kwargs.items():
        setattr(entry, key, value)
    return jsonify(model_schema().dump(entry))


@db_lifecycle
@session_lifecycle
def delete_entry_by_id(model_class, model_schema, id):  # DELETE entity by id
    entry = session.query(model_class).filter_by(id=id).first()
    if entry is None:
        raise InvalidUsage("Object not found", status_code=404)
    session.delete(entry)
    return jsonify(model_schema().dump(entry))


