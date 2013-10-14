import tornado.web
import tornado.websocket
import tornado.ioloop
import os

host=os.environ['IP']
port=os.environ['PORT']

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/sliderssocket", SlidersSocket),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html");
        
class SlidersSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        self.write_message(u"You said: " + message )

    def on_close(self):
        print "WebSocket closed"


if __name__ == "__main__":
    app = Application()
    app.listen(port, host)
    tornado.ioloop.IOLoop.instance().start()