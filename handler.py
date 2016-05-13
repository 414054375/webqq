#coding:utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import config
import models
from lsqlite import db
import random
import os.path
#处理登录的cookie的子类，继承BaseHandler

class BaseHandler(tornado.web.RequestHandler):
    def get_current_id(self):
        a = self.get_secure_cookie(config._id)
        return a
    def set_current_id(self, id):
        self.set_secure_cookie(config._id, id)

#给LoginHandler辅助，承上启下
class LoginCookieHandler(BaseHandler):
    def login(self,id,password):
        a = db.select("select * from user where ID = ? and password = ?", id,password)
        if len(a)==1:
            self.set_current_id(id)      
            if models.Check_Friend_Table(id)==0:
                m = models.New_Friend_Table(id)
                print m.__table__
                print type(m.__table__)
                db.update('drop table if exists %s' %  m.__table__ )
                db.update(m().__sql__())
            #在live中通过cookie获取好友列表
            self.redirect("/live",permanent = True)#跳转到listHandler get
        elif len(a)==0:
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"用户名或密码错误\"); window.history.back()</script></html>")
        else:
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"系统错误\"); window.history.back()</script></html>")
    def logout(self):
        self.clear_cookie(config._id)
    def post(self):
        self.logout()
        self.redirect("/login",permanent = True)

class LoginHandler(LoginCookieHandler):
    def get(self):
        print db.select("select * from user")
        self.render("login.html")
    def post(self):
        id = self.get_argument(config._id)#用户id
        password = self.get_argument(config._password)#用户密码
        self.login(id,password)

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        #判定密码重复情况
        password1 = self.get_argument("password1")
        password2 = self.get_argument("password2")
        nickname = self.get_argument("nickname")
        if (password1!=password2):
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"两次密码不相同\"); window.history.back()</script></html>")
            return
        #随机用户id
        a = [0]#让a不为空
        while (len(a)!=0):
            id = random.randint(100000,999999)
            a = db.select("select * from user where ID = ?",id)
        models.UserTable(ID = id,password = password1,nickname = nickname).insert()
        #跳转到登录成功界面
        self.render("register_success.html",id = id) 

class LiveHandler(BaseHandler):
    def get(self):
        id = self.get_current_id()
        if (id is None):#用cookie判断是否登录
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"请登录\"); window.history.back()</script></html>")
            return
        u = models.UserTable.query(id)
        Friends_id = models.Get_Friends(id)
        print Friends_id
        self.render("live.html",id = id,nickname = u[0]['nickname'],friends = Friends_id)