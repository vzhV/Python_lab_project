from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime, Boolean
import enum
from sqlalchemy import Enum
from sqlalchemy import DECIMAL

engine = create_engine('mysql+pymysql://root:zh683099@localhost/pplab7')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()
BaseModel.query = Session.query_property()

class MyEnum(enum.Enum):
    teacher = 'teacher'
    student = 'student'


class User(BaseModel):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(45))
    email = Column(VARCHAR(45), unique=True)
    password = Column(VARCHAR(10000))
    position = Column(Enum(MyEnum))

    def __str__(self):
        return f"userID    : {self.id}\n" \
               f"name      : {self.name}\n" \
               f"email     : {self.email}\n" \
               f"password  : {self.password}\n" \
               f"position  : {self.position}\n"


class Course(BaseModel):
    __tablename__ = 'Course'

    id = Column(Integer, primary_key=True)
    subject = Column(VARCHAR(45))
    teacherID = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"))
    def subj(self):
        return self.subject
    def t(self):
        return self.teacherID
    def __str__(self):
        return f"courseID : {self.id}\n" \
               f"Subject : {self.subject}\n" \
               f"teacherID : {self.teacherID}\n"




class JoinRequest(BaseModel):
    __tablename__ = 'Join Request'

    id = Column(Integer, primary_key=True)
    studentID = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"))
    courseID = Column(Integer, ForeignKey(Course.id, onupdate="CASCADE", ondelete="CASCADE"))
    access = Column(Boolean, default=False)

    def __str__(self):
        return f"RequestID : {self.id}\n" \
               f"userID : {self.userID}\n" \
               f"CourseID : {self.courseID}\n"





# Використання міграції : alembic upgrade head
