# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf8")

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options
from autoloads import app


def main():
    app.scan(options.scan_handlers_path)
    application = tornado.web.Application(app(), **options.as_dict())
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()