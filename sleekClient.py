#CONFIGURE HERE

boturl="http://127.0.0.1:5001/sendMessage"
clientID='alexuidian1@jabb.im'
serverhost="jabb.im"
clientPass='21101991'




from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import threading
import ssl
import time
from flask import Flask
#from quart import Quart
from flask import request
import json
import asyncio
app = Flask(__name__)
import time

#loop=asyncio.get_event_loop()


@app.route("/sendMessage2", methods = ['GET', 'POST', 'DELETE'])
#format: Post Method {'uid' : 'userid', 'message' : 'message here', 'timestamp:' 'timestamp here'}
def sendMessage2():
#	print(request.form)
#	print(request.args)
	global boturl 
	global clientID
	global serverhost
	global clientPass
	message=request.get_json()
	user=message['uid']
	body=message['message']
	timestamp=str(time.time())
	if 'timestamp' in message.keys():
		timestamp=message['timestamp']
	#a=threading.Thread(target=send_finally, args=(clientID, clientPass, user+'@'+serverhost, body) )
	#a.start()
	send_finally2(clientID, clientPass, user+'@'+serverhost, body )
	#a.deamon(True)
	#asyncio.run()
	#sending=sendMessageClass(clientID, clientPass, user+'@'+serverhost, body)
	#asyncio.run(sending.processme())
	return "Hello, World!"

def send_finally2(clientID, clientPass, user, body):
	sending=sendMessageClass(clientID, clientPass, user, body)
	sending.connect()
	sending.process()

	
@app.route("/sendMessage", methods = ['GET', 'POST', 'DELETE'])
#format: Post Method {'uid' : 'userid', 'message' : 'message here', 'timestamp:' 'timestamp here'}
def sendMessage():
#	print(request.form)
#	print(request.args)
	global boturl 
	global clientID
	global serverhost
	global clientPass
	message=request.get_json()
	user=message['uid']
	body=message['message']
	timestamp=str(time.time())
	if 'timestamp' in message.keys():
		timestamp=message['timestamp']
	#a=threading.Thread(target=send_finally, args=(clientID, clientPass, user+'@'+serverhost, body) )
	#a.start()
	asyncio.run(send_finally(clientID, clientPass, user+'@'+serverhost, body ))
	#a.deamon(True)
	#asyncio.run()
	#sending=sendMessageClass(clientID, clientPass, user+'@'+serverhost, body)
	#asyncio.run(sending.processme())
	return "Hello, World!"

async def send_finally(clientID, clientPass, user, body):
	sending=sendMessageClass(clientID, clientPass, user, body)
	await sending.processme()
	


class EchoBot(ClientXMPP):
	
	def __init__(self, jid, password):
		self.conn=ClientXMPP.__init__(self, jid, password, handlefunction=self.message )
		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		print("Setup Done")

	def session_start(self, event):
		self.send_presence()
		self.get_roster()

	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			msg.reply("Thanks for sending\n%(body)s" % msg).send()
	


class sendMessageClass(ClientXMPP):
	def __init__(self, jid, password, mto, mbody):
		ClientXMPP.__init__(self, jid, password)
		self.mto=mto
		self.mbody=mbody
		self.add_event_handler("session_start", self.start)

	def start(self, event):
		self.send_presence()
		self.get_roster()
		self.send_message(mto=self.mto, mbody=self.mbody, mtype='chat')
		self.disconnect(wait=True)
	async def processme(self):
		self.connect()
		self.process()



if __name__ == "__main__":
        
    app.run(host='0.0.0.0', port='5001', debug=True )
