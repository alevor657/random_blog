import tornado.ioloop
import tornado.web
import database
from database import Posts, Categories

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hi there!')

class PostsGetHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        if id == None:
            result = db.get_all()
            posts = []
            for r in result:
                posts.append(r.toDict())

            self.write({'posts' : posts})

        else:
            try:
                result = db.get(id)
                self.write(result.toDict())
            except:
                self.send_error(404)

class PostsPutHandler(tornado.web.RequestHandler):
    def get(self):
        header = self.get_argument('header')
        content = self.get_argument('content')
        author =  self.get_argument('author')
        categories = self.get_arguments('categories')
        post = Posts(header, content, author, categories)
        db.add(post)

class PostsUpdateHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        header = self.get_argument('header', default = None)
        content = self.get_argument('content', default = None)
        author =  self.get_argument('author', default = None)
        #categories = self.get_arguments('categories', default = None)
        categories = None
        post = Posts(header, content, author, categories, id)
        db.update(post)

class PostsDeleteHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        db.delete(id)

class CategoriesHandler(tornado.web.RequestHandler):
    def get(self):
        categories = []
        result = db.get_categories()
        for r in result:
            categories.append(r.toDict())

        self.write({'categories': categories})

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts/get', PostsGetHandler),
        (r'/posts/get/(\d+)', PostsGetHandler),
        (r'/posts/add', PostsPutHandler),
        (r'/posts/update/(\d+)', PostsUpdateHandler),
        (r'/posts/delete/(\d+)', PostsDeleteHandler),
        (r'/categories/get', CategoriesHandler)
    ])


if __name__ == "__main__":
    db = database.DB()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
