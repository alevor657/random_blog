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
                   lazy = 'subquery'
                   #back_populates = 'parents'
                   )

class Categories(Base):
    __tablename__ = 'categories'
    category = Column(String, primary_key = True)

    posts = relationship('Posts',
                    secondary = posts_to_categories_table,
                    #back_populates = 'children'
                    )

class DB():
    connect_str = 'postgresql+psycopg2://user:user@localhost:5432/blog'
    engine = create_engine(connect_str)
    DBSession = sessionmaker(bind = engine)

    def add(self):
        pass

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

    def update(self):
        pass
