from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    position = fields.String()

class CourseSchema(Schema):
    id = fields.Integer()
    teacherID = fields.Integer()
    subject = fields.String()

class JoinRequestSchema(Schema) :
    id = fields.Integer()
    studentID = fields.Integer()
    courseID = fields.Integer()
    access = fields.Boolean();

