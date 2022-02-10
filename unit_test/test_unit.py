import unittest
from RestApiImplementation.app import app
import json
from base64 import b64encode
from sqlalchemy.orm import sessionmaker
from RestApiImplementation.utils_db import bcrypt
from RestApiImplementation.au import verify_password
from RestApiImplementation.models_api import User,Course,JoinRequest, engine, MyEnum

Session = sessionmaker(bind = engine)

class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
    app_context = app.app_context()
    app_context.push()
    tester = app.test_client()
    session = Session()

    def tearDown(self):
        self.close_session()
    def close_session(self):
        self.session.close()

class ApiTest(TestingBase):
    student = {
        "id":123,
        "name": "Vova",
        "email":"02@gmail.com",
        "password":"1111",
        "position": "student"
    }
    teacher = {
        "id":785,
        "name": "Valentyn",
        "email": "03@gmail.com",
        "password": "1111",
        "position": "teacher"
    }
    course = {
        "id":14,
        "subject":"Math",
        "teacherID" : 787
    }
    course2 = {
        "id": 14,
        "subject": "Math",
        "teacherID": None
    }
    join = {
        "id":4,
        "courseID":101,
        "studentID":8999,
    }

    def test_student_creation(self):
        response = self.tester.post("/user", data = json.dumps(self.student), content_type = "application/json")
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(User).filter_by(email="02@gmail.com").delete()
        self.session.commit()

    def test_teacher_creation(self):
        response = self.tester.post("/user", data = json.dumps(self.teacher), content_type = "application/json")
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(User).filter_by(email = "03@gmail.com").delete()
        self.session.commit()

    def test_get_user_by_id_invalid(self):
        response = self.tester.get("/user/175")
        code = response.status_code
        self.assertEqual(500, code)

    def test_get_users(self):
        response = self.tester.get("/user")
        code = response.status_code
        self.assertEqual(200, code)

    def test_get_user_by_id(self):
        response = self.tester.get("/user/2")
        code = response.status_code
        self.assertEqual(500, code)

    def test_post_join(self):
        response = self.tester.post("/joinrequest", data=json.dumps(self.join), content_type="application/json")
        code = response.status_code
        self.assertEqual(500, code)
        self.session.query(JoinRequest).filter_by(id = 4).delete()
        self.session.commit()


    def test_update_user(self):
        hashpassword = bcrypt.generate_password_hash('1111')
        user = User(id = 90, name = "Alex", position = "teacher", email = "90@gmail.com", password = hashpassword)
        self.session.add(user)
        self.session.commit()
        cred = b64encode(b"90@gmail.com:1111").decode("utf-8")
        response = self.tester.put("/user", data = json.dumps({"name":"Arhangel", "email":"90@gmail.com", "password":"1111","position":"teacher"}), content_type = 'application/json', headers={"Authorization":f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(User).filter_by(email="90@gmail.com").delete()
        self.session.commit()

    def test_delete_user(self):
        cred = b64encode(b"90@gmail.com:1111").decode("utf-8")
        response = self.tester.delete("/user", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_course_creation(self):
        hashpassword = bcrypt.generate_password_hash('1111')
        user = User(id=90, name="Alex", position="teacher", email="90@gmail.com", password=hashpassword)
        self.session.add(user)
        self.session.commit()
        cred = b64encode(b"90@gmail.com:1111").decode("utf-8")
        response = self.tester.post("/course", data = json.dumps(self.course), content_type = "application/json", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(Course).filter_by(id=14).delete()
        self.session.commit()
        self.session.query(User).filter_by(email="90@gmail.com").delete()
        self.session.commit()

    def test_course_creation2(self):
        hashpassword = bcrypt.generate_password_hash('1111')
        user = User(id=90, name="Alex", position="teacher", email="90@gmail.com", password=hashpassword)
        self.session.add(user)
        self.session.commit()
        cred = b64encode(b"90@gmail.com:1111").decode("utf-8")
        response = self.tester.post("/course", data = json.dumps(self.course2), content_type = "application/json", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(Course).filter_by(id=14).delete()
        self.session.commit()
        self.session.query(User).filter_by(email="90@gmail.com").delete()
        self.session.commit()

    def test_join_update(self):
        response = self.tester.post("/joinrequest", data=json.dumps(self.join), content_type="application/json")
        response = self.tester.put("/joinrequest/4", data = json.dumps({"id":4,"studentID":786,"courseID":404,"access":True}))
        self.assertEqual(500,response.status_code)
        self.session.query(JoinRequest).filter_by(id=4).delete()
        self.session.commit()

    def test_get_courses(self):
        cred = b64encode(b"1000@gmail.com:1111").decode("utf-8")
        response = self.tester.get("/course", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_course_update(self):
        hashpassword = bcrypt.generate_password_hash('1111')
        user = User(id=90, name="Alex", position="teacher", email="90@gmail.com", password=hashpassword)
        self.session.add(user)

        cred = b64encode(b"90@gmail.com:1111").decode("utf-8")
        response = self.tester.put("/course/101", data = json.dumps({"id":101,"subject":"physic","teacherID":787}), content_type = "application/json", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(Course).filter_by(id=101).delete()
        self.session.commit()
        self.session.query(User).filter_by(email="90@gmail.com").delete()
        self.session.commit()

    def test_course_creation3(self):
        cred = b64encode(b"999@gmail.com:1111").decode("utf-8")
        response = self.tester.post("/course", data = json.dumps(self.course), content_type = "application/json", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(200,code)
        self.session.query(Course).filter_by(id=14).delete()
        self.session.commit()

    def test_get_course(self):
        cred = b64encode(b"1000@gmail.com:1111").decode("utf-8")
        response = self.tester.get("/course/14", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(500, code)

    def test_delete_course(self):
        cred = b64encode(b"1000@gmail.com:1111").decode("utf-8")
        response = self.tester.get("/course/14", headers={"Authorization": f"Basic {cred}"})
        code = response.status_code
        self.assertEqual(500, code)








