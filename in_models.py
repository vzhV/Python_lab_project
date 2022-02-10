from models import Session, JoinRequest, Course, User
session = Session()

USER_1 = User(id = 1, name = 'John', email = 'user1@gmail.com', password = "12345678", position = "student")
USER_2 = User(id = 2, name = 'Jack', email = 'user2@gmail.com', password = "12345678", position = "teacher")
USER_3 = User(id = 56, name = 'Jerry', email = 'user3@gmail.com', password = 'sdklashdlsak', position = 'student')

Course_1 = Course(id = 1, subject = 'Math', teacherID = 2)


Join_1 = JoinRequest(id = 1, studentID = 1, courseID = 1)
Join_2 = JoinRequest(id = 42, studentID = 56, courseID = 1)

session.add(USER_1)
session.add(USER_2)
session.add(USER_3)
session.commit()
session.add(Course_1)
session.commit()
session.add(Join_1)
session.add(Join_2)
session.commit()


session.commit()

print(session.query(User).all()[0])
print(session.query(Course).all())
print(session.query(JoinRequest).all())

session.close()
