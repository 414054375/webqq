import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
import random
import config
from lsqlite import db
import models
from handler import LoginHandler,RegisterHandler,LiveHandler,LoginCookieHandler
from server_socket import SocketHandler
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login", LoginHandler),
            (r"/register",RegisterHandler),
            (r"/live",LiveHandler),
            (r"/soc",SocketHandler),
            (r"/logout",LoginCookieHandler),
        ]
        settings = config.settings
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    db.create_engine(config.database)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.webport)
    tornado.ioloop.IOLoop.instance().start()