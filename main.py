import tornado.ioloop
import tornado.web
import database
from database import Posts, Categories

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hi there!')

class PostsHandler(tornado.web.RequestHandler):
    def get(self, id = None):
        if id == None:
            result = db.get_all()
            posts = []
            for r in result:
                posts.append(to_dict(r))

            self.write({'posts' : posts})

        else:
            result = db.get(id)
            self.write(to_dict(result))

class CategoryHandler(tornado.web.RequestHandler):
    pass

def to_dict(post : Posts):
    ctgs = []
    for c in post.categories:
        ctgs.append(c.category)

    return {
        'id' : post.id,
        'header' : post.header,
        'content' : post.content,
        'creation_date' : post.creation_date,
        'modification_date' : post.modification_date,
        'deletion_date' : post.deletion_date,
        'author' : post.author,
        'categories' : ctgs
    }


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts/get', PostsHandler),
        (r'/posts/get/(\d+)', PostsHandler),
    ])


if __name__ == "__main__":
    db = database.DB()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
