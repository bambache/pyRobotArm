import tornado.web
import tornado.websocket
import tornado.ioloop
import os
import sys
import serial
import time
import threading

host=os.environ['IP']
port=os.environ['PORT']

PORT = "loop://logging=debug"
#PORT = "/dev/ttyACM0"
TIMEOUT = 1

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
    def __init__(self, app, request, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, app, request, **kwargs)
        self.serial = serial.serial_for_url(PORT, timeout=TIMEOUT)
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(True)
        self.thread_read.setName('read serial')
        self.thread_read.start()

    def reader(self):
        """loop forever """
        while self.alive:
            try:
                data = self.serial.readline() # read one line, blocking
                if data:
                    self.write_message(u'received: <' + data + '>')
                    # here some parsing is done, to get the real positions for the sliders, as feedback from arduino
                    #values = data.decode().split(',')
                    #assert (len(values) == NMB_OF_SLIDERS)
                    #for i in range(NMB_OF_SLIDERS):
                    #  self.sliders[i].set(int(values[i]))
            except:
                sys.stderr.write('ERROR: %s\n' % sys.exc_info()[0] )
                raise
        self.alive = False
    
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        self.write_message(u"Sending to Serial port: <" + message +">")
        self.serial.write(message+'\n')

    def on_close(self):
        print "WebSocket closed"


if __name__ == "__main__":
    app = Application()
    app.listen(port, host)
    tornado.ioloop.IOLoop.instance().start()