from sqlalchemy import Column, create_engine, Table, ForeignKey
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

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
                              lazy = 'subquery'
                              )

    def __init__(self, header = None, content = None, author = None,
                 categories = None, id = None):
        self.id = id
        self.header = header
        self.content = content
        self.creation_date = datetime.now()
        self.author = author
        if categories != None:
            for c in categories:
                category = Categories(category = c)
                self.categories.append(category)

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

class Categories(Base):
    __tablename__ = 'categories'
    category = Column(String, primary_key = True)

    posts = relationship('Posts',
                    secondary = posts_to_categories_table,
                    )

    def toDict(self):
        return {
            'category' : self.category
        }

class DB():
    connect_str = 'postgresql+psycopg2://user:user@localhost:5432/blog'
    engine = create_engine(connect_str)
    DBSession = sessionmaker(bind = engine)

    def add(self, post : Posts):
        session = self.DBSession()
        session.add(post)
        session.commit()
        session.close()

    def get_all(self):
        session = self.DBSession()
        result = session.query(Posts).join(Posts.categories).all()
        session.close()
        return result

    def get(self, id):
        session = self.DBSession()
        result = session.query(Posts).join(Posts.categories).\
            filter(Posts.id == id).first()
        session.close()
        return result

    def delete(self):
        pass

    def update(self, np : Posts):
        if np.id == None:
            return
        session = self.DBSession()
        post = session.query(Posts).filter(Posts.id == np.id)
        if np.header != None:
            post.update({'header':np.header})
        if np.content != None:
            post.update({'content':np.content})
        if np.author != None:
            post.update({'author':np.author})
        #if not np.categories
            #post.categories = np.categories
        post.update({'modification_date':datetime.now()})
        session.commit()
        session.close()

    def get_categories(self):
        session = self.DBSession()
        result = session.query(Categories).all()
        session.close()
        return result
