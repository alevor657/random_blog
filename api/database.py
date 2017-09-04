from sqlalchemy import Table, Column, ForeignKey, create_engine
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload, subqueryload
from datetime import datetime

Base = declarative_base()
with open('connect_str.txt', 'r', encoding = 'utf-8') as file:
    line = file.read()
    connect_str = line.rstrip()
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
                              lazy = 'joined'
                             )

    def __init__(self, header = None, content = None, author = None, id = None):
        self.id = id
        self.header = header
        self.content = content
        self.creation_date = datetime.now().replace(microsecond=0).isoformat(' ')
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
        post.deletion_date = datetime.now().replace(microsecond=0).isoformat(' ')
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

        post.modification_date = datetime.now().replace(microsecond=0).isoformat(' ')
        session.commit()
        session.close()

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    category = Column(String, nullable = False)

    posts = relationship('Posts',
                         secondary = posts_to_categories_table,
                         primaryjoin = "Categories.id == posts_to_categories.c.category",
                         secondaryjoin = "and_(posts_to_categories.c.posts_id == Posts.id, "
                                         "Posts.is_deleted == False)"
                         )

    def __init__(self, category = None, id = None):
        self.category = category

    def toDict(self):
        return {
            'id' : self.id,
            'category' : self.category
        }

    def get(id):
        session = DBSession()
        category = session.query(Categories).get(id)
        session.close()
        return category

    def get_all():
        session = DBSession()
        result = session.query(Categories).all()
        session.close()
        return result
    #shit
    def get_posts(id):
        session = DBSession()
        category = session.query(Categories).\
                   options(joinedload('posts').joinedload('categories')).\
                   get(id)
        result = category.posts
        session.close()
        return result

    def add(category):
        session = DBSession()
        session.add(category)
        session.commit()
        session.close()
