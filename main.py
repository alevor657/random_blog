import tornado.ioloop
import tornado.web

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hi there!')

def make_app():
    return tornado.web.Application([
        (r'/hi', TestHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
