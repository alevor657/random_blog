from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Posts(Base):
    pass

class Categories(Base):
    pass

class DB():
    connect_str = 'postgresql+psycopg2://user:user@localhost:5432/'
    engine = create_engine(connect_str)
    DBSession = sessionmaker(bind = engine)

    def add(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
