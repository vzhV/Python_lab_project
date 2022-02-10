from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, DateTime, Boolean
import enum
from sqlalchemy import Enum
from sqlalchemy import DECIMAL
Base = declarative_base()
metadata = Base.metadata
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


class Course(BaseModel):
    __tablename__ = 'Course'

    id = Column(Integer, primary_key=True)
    subject = Column(VARCHAR(45))
    teacherID = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"))


class JoinRequest(BaseModel):
    __tablename__ = 'Join Request'

    id = Column(Integer, primary_key=True)
    studentID = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"))
    courseID = Column(Integer, ForeignKey(Course.id, onupdate="CASCADE", ondelete="CASCADE"))
    access = Column(Boolean, default=False)



# Використання міграції : alembic upgrade head
