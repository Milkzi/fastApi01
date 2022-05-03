from sqlalchemy import create_engine, String, Integer, Boolean, Column, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from setting import SQLALCHEMY_DATABASE_URI
from sqlalchemy.pool import QueuePool

engine = create_engine(url=SQLALCHEMY_DATABASE_URI,
                       pool_size=10,
                       max_overflow=5,
                       pool_timeout=10,
                       pool_pre_ping=True,
                       pool_recycle=120,
                       poolclass=QueuePool,
                       )

base_model = declarative_base()


class FengData(base_model):
    __tablename__ = "feng_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(500), unique=True, nullable=False)
    code = Column(String(100), default=None, unique=True)
    check_status = Column(String(10), default="")
    is_status = Column(Boolean, default=False)


class DeleteFengData(base_model):
    __tablename__ = "delete_feng_data_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(500), nullable=False)
    code = Column(String(100), default=None)
    check_status = Column(String(10), default="")
    is_status = Column(Boolean, default=False)
    insert_time = Column(DateTime)


session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db_session = scoped_session(session_factory=session_factory)
