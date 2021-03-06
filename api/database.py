from sqlalchemy import Table, Column, ForeignKey, create_engine
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
connect_str = 'postgresql+psycopg2://user:user@localhost:5432/blog'
engine = create_engine(connect_str)
DBSession = sessionmaker(bind = engine)

#association table
posts_to_categories_table = Table('posts_to_categories', Base.metadata,
    Column('posts_id', Integer, ForeignKey('posts.id')),
    Column('category', Integer, ForeignKey('categories.id'))
)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    header = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    creation_date = Column(DateTime, nullable = False)
    modification_date = Column(DateTime, nullable = True)
    deletion_date = Column(DateTime, nullable = True)
    is_deleted = Column(Boolean, nullable = False)
    author = Column(String, nullable = False)

    categories = relationship('Categories',
                              secondary = posts_to_categories_table,
                              lazy = 'subquery'
                             )

    def __init__(self, header = None, content = None, author = None, id = None):
        self.id = id
        self.header = header
        self.content = content
        self.creation_date = datetime.now()
        self.author = author
        self.is_deleted = False

    def toDict(self):
        ctgs = []
        for c in self.categories:
            ctgs.append(c.category)

        return {
            'id' : self.id,
            'header' : self.header,
            'content' : self.content,
            'creation_date' : str(self.creation_date),
            'modification_date' : str(self.modification_date),
            'deletion_date' : str(self.deletion_date),
            'author' : self.author,
            'categories' : ctgs
        }

    def add(post, categories):
        session = DBSession()
        session.add(post)
        for id in categories:
            category = session.query(Categories).get(id)
            post.categories.append(category)
        session.commit()
        session.close()

    def get_all():
        session = DBSession()
        result = session.query(Posts).filter(Posts.is_deleted == False).\
                 order_by(Posts.id).all()
        session.close()
        return result

    def get(id):
        session = DBSession()
        post = session.query(Posts).filter(Posts.id == id,
                 Posts.is_deleted == False).one()
        session.close()
        return post

    def delete(id):
        session = DBSession()
        post = session.query(Posts).filter(Posts.id == id,
                 Posts.is_deleted == False).one()
        post.is_deleted = True
        post.deletion_date = datetime.now()
        session.commit()
        session.close()

    def update(new_post, categories):
        session = DBSession()
        post = session.query(Posts).filter(Posts.id == new_post.id,
                 Posts.is_deleted == False).one()

        if new_post.header != None:
            post.header = new_post.header
        if new_post.content != None:
            post.content = new_post.content
        if new_post.author != None:
            post.author = new_post.author
        if categories:
            post.categories.clear()
            for c in categories:
                category = session.query(Categories).get(c)
                post.categories.append(category)

        post.modification_date = datetime.now()
        session.commit()
        session.close()

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    category = Column(String, nullable = False)

    posts = relationship('Posts',
                         secondary = posts_to_categories_table)

    def __init__(self, category = None, id = None):
        self.category = category

    def toDict(self):
        return {
            'id' : self.id,
            'category' : self.category
        }

    def get_all():
        session = DBSession()
        result = session.query(Categories).all()
        session.close()
        return result

    def add(category):
        session = DBSession()
        session.add(category)
        session.commit()
        session.close()
