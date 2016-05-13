#coding:utf-8
import tornado.websocket
import handler
from handler import BaseHandler
import config
class SocketHandler(tornado.websocket.WebSocketHandler):
	clients_on = dict()
	@staticmethod
	def send_to(id,message):
		'''
		单人聊天标准格式应该为 
		for id in SocketHandler.clients_on[char_id]:
		    user = SocketHandler.clients_on[id]
		    user.write
		多人聊天需要用SocketHandler.clients_on[char_id]去找群号，用db.select找出群号对应的所有人的id，然后同样的循环
		或者这里在读到Group的时候处理clients_on
		'''
		a = SocketHandler.clients_on["chat_"+ id]
		print a
		print SocketHandler.clients_on
		user = SocketHandler.clients_on[a]
		print user
		print type(user)
		print message
		print type(message)

		user.write_message(message)

	def open(self):
		id = self.get_secure_cookie(config._id)
		print "open id:",id
		SocketHandler.clients_on[id]=self
		print SocketHandler.clients_on
#类方法和静态方法都可以被类和类实例调用，类实例方法仅可以被类实例调用
#类方法的隐含调用参数是类，而类实例方法的隐含调用参数是类的实例，静态方法没有隐含调用参数
	def on_close(self):
		#SocketHandler.clients.remove(self)
		id = self.get_secure_cookie(config._id)
		print "close id:",id
		del SocketHandler.clients_on[id]
		print SocketHandler.clients_on

	def on_message(self,data):
		'''
		传回的信息有以下几种
		如果本端id为10000
		（开头为F-Friends）F10001 表示需要连接的朋友id，需要更新clients_on["chat_10000"]=10001
		（开头为C-content）C你好 表示需要发送的信息，向clients_on["chat_10000"]中的用户发送
								伪代码如下：
								for user in SocketHandler.clients_on["chat_10000"]:
									rec = SocketHandler.clients_on[user]
									rec.write(message)

		'''
		id = self.get_secure_cookie(config._id)
		print "message id ",id
		print "on_message data:",data
		if data[0]=="F":
			self.create_connection(str(id),data)#自动过滤选择不同的函数处理
		elif data[0]=="C":
			self.send_to(str(id),data[1:])

	def create_connection(self,id,data):
		print "create_connection: id data",id,data
		if data[0]=="F":
			f_id = data[1:]
			SocketHandler.clients_on["chat_"+id] = f_id
			print SocketHandler.clients_on


