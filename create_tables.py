from sqlalchemy import Column, create_engine, Table, ForeignKey
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

posts_to_categories_table = Table('posts_to_categories', Base.metadata,
    Column('posts_id', Integer, ForeignKey('posts.id')),
    Column('category', String, ForeignKey('categories.category'))
)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    header = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    creation_date = Column(DateTime, nullable = True)
    modification_date = Column(DateTime, nullable = True)
    deletion_date = Column(DateTime, nullable = True)
    author = Column(String, nullable = False)

    categories = relationship('Categories',
                   secondary = posts_to_categories_table,
                   #backref = 'parents'
                   )

class Categories(Base):
    __tablename__ = 'categories'
    category = Column(String, primary_key = True)

    posts = relationship('Posts',
               secondary = posts_to_categories_table)

connect_str = 'postgresql+psycopg2://user:user@localhost:5432/blog'
engine = create_engine(connect_str)
DBSession = sessionmaker(bind = engine)

#create tables
#Base.metadata.create_all(engine)

session = DBSession()
post = Posts(header = 'header2', content = 'cotent2', author = 'author2')
category = Categories(category = 'category1')
category2 = Categories(category = 'category2')
post.categories.append(category)
post.categories.append(category2)
session.add(post)
session.commit()
