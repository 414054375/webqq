import tornado.websocket
class SocketHandler(tornado.websocket.WebSocketHandler):
	clients = set()
	@staticmethod
	def send_to_all(message):
		for c in SocketHandler.clients:
			c.write_message(message)

	def open(self):
		SocketHandler.clients.add(self)

	def on_close(self):
		SocketHandler.clients.remove(self)

	def on_message(self,data):
		SocketHandler.send_to_all(data)