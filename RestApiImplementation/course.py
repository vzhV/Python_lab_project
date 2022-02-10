from RestApiImplementation.models_api import Course
from RestApiImplementation.models_api import User
from RestApiImplementation.au import verify_password, auth
from RestApiImplementation.schemas import CourseSchema
from flask import request
from flask import Blueprint
from flask import Response
# from flask_httpauth import HTTPBasicAuth
from RestApiImplementation.models_api import Session
from RestApiImplementation.utils_db import (
    create_entry,
    get_entries,
    get_entry_by_id,
    get_course_by_id,
    delete_entry_by_id,
    InvalidUsage
)

course = Blueprint("course", __name__)
session = Session()


# auth = HTTPBasicAuth()
@course.route("/course", methods=["POST"])  # create new auditorium
@auth.login_required()
def create_course():
    user = session.query(User).filter_by(email=auth.current_user()).first()
    if str(user.position) == "MyEnum.teacher":
        course_data = CourseSchema().load(request.get_json())

        return create_entry(Course, CourseSchema, **course_data)

    else:
        raise InvalidUsage("You don't have acces to perform this operation", status_code=403)


@course.route("/course", methods=["GET"])  # get all auditoriums
@auth.login_required
def get_course():
    return get_entries(Course, CourseSchema)


@course.route("/course/<int:id>", methods=["GET"])  # get auditorium by id
@auth.login_required
def get_cours_by_id(id):
    # user = session.query(User).filter_by(email=auth.current_user()).first()
    # if str(user.position) == "MyEnum.teacher":
    return get_entry_by_id(Course, CourseSchema, id)
    # else:
    #     return get_course_by_id(id, user.id)


@course.route("/course/<int:id>", methods=["PUT"])  # update auditorium by id
@auth.login_required
def update_entry_by_id(id):
    user = User.query.filter_by(email="1000@gmail.com").first()
    if str(user.position) == "MyEnum.teacher":
        course_data = CourseSchema().load(request.get_json())
        course = session.query(Course).filter_by(id=id).first()
        if course is None:
            raise InvalidUsage("Object not found", status_code=404)
        tempD = {'id': course.id, 'subject': course.subject, 'teacherID': course.teacherID}
        for key, value in course_data.items():
            tempD[key] = value
        print(tempD)
        delete_entry_by_id(Course, CourseSchema, id)
        return create_entry(Course, CourseSchema, **tempD)
    else:
        raise InvalidUsage("You don't have acces to perform this operation", status_code=403)

    # return update_entry_by_id(Course, CourseSchema, id, **course_data)


@course.route("/course/<int:id>", methods=["DELETE"])  # delete auditorium by id
@auth.login_required
def delete_course_by_id(id):
        return delete_entry_by_id(Course, CourseSchema, id)


