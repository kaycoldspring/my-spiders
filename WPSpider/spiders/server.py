# -*- coding: utf-8 -*-
# @Time    : 2020/7/23 11:52
# @Author  : Kay Luo
# @FileName: server.py
# @Software: PyCharm


import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])





if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()