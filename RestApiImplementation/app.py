from flask import Flask
from RestApiImplementation.Session import sesion
from RestApiImplementation.user import user
from RestApiImplementation.course import course
from RestApiImplementation.JoinRequest import join
app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(sesion)
app.register_blueprint(course)
app.register_blueprint(join)


@app.route("/api/v1/hello-world-7")
def index():
    return "Hello World 7!"

