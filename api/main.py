import tornado.ioloop
import tornado.web
import database
from database import Posts, Categories

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(help_page)

class PostsGetHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        if id == None:
            result = Posts.get_all()
            posts = []
            for post in result:
                posts.append(post.toDict())
            self.write({'posts' : posts})
        else:
            try:
                post = Posts.get(id)
                self.write(post.toDict())
            except:
                self.send_error(400)

class PostsAddHandler(tornado.web.RequestHandler):
    def get(self):
        header = self.get_argument('header')
        content = self.get_argument('content')
        author =  self.get_argument('author')
        categories = self.get_arguments('categories')
        if not categories:
            self.send_error(400)
        else:
            post = Posts(header, content, author)
            Posts.add(post, categories)

class PostsUpdateHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        header = self.get_argument('header', default = None)
        content = self.get_argument('content', default = None)
        author =  self.get_argument('author', default = None)
        categories = self.get_arguments('categories')
        post = Posts(header, content, author, id)
        try:
            Posts.update(post, categories)
        except:
            self.send_error(400)

class PostsDeleteHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        try:
            Posts.delete(id)
        except:
            self.send_error(400)

class CategoriesGetHandler(tornado.web.RequestHandler):
    def get(self):
        categories = []
        result = Categories.get_all()
        for category in result:
            categories.append(category.toDict())

        self.write({'categories': categories})

class CategoriesAddHandler(tornado.web.RequestHandler):
    def get(self):
        category = self.get_argument('category')
        ctg = Categories(category)
        Categories.add(ctg)

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts/get', PostsGetHandler),
        (r'/posts/get/(\d+)', PostsGetHandler),
        (r'/posts/add', PostsAddHandler),
        (r'/posts/update/(\d+)', PostsUpdateHandler),
        (r'/posts/delete/(\d+)', PostsDeleteHandler),
        (r'/categories/get', CategoriesGetHandler),
        (r'/categories/add', CategoriesAddHandler)
    ])


if __name__ == "__main__":
    with open('help.txt', 'r', encoding = 'utf-8') as file:
        help_page = file.read()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
