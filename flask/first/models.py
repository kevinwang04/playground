from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255))

class User(Base):
    __tablename__ = 'userss'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(32), nullable=False, unique=True, server_default='', index=True)
    role_id = Column(Integer, nullable=False, server_default='0')

class Category(Base):
    __tablename__ = 'categoris'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,unique=True)
    name = Column(String(32), nullable=False, unique=True, server_default='--')
    sort = Column(Integer, nullable=False, server_default='0') 
    description = Column(String(32), nullable=True, unique=False) 

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)