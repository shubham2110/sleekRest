#CONFIGURE HERE

boturl="http://127.0.0.1:5002/sendMessage"
clientID='alexuidian1@jabb.im'
serverhost="jabb.im"
clientPass='21101991'

clientID='basis@10.52.150.150'
clientPass='Cois@12345'
serverhost='indianoil'
logfile='log.txt'

clientID='basis@jabb.im'
clientPass='21101991'
serverhost='jabb.im'
logfile='log.txt'



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
from browser3 import browser

#loop=asyncio.get_event_loop()


@app.route("/sendMessage2", methods = ['GET', 'POST', 'DELETE'])
#format: Post Method {'uid' : 'userid', 'message' : 'message here', 'timestamp:' 'timestamp here'}
def sendMessage2():
#	print(request.form)
#	print(request.args)
#	global boturl 
#	global clientID
#	global serverhost
#	global clientPass
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
	return "Done."

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
	#print("Request came for user:", user)
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
		self.mids=[]
		print("Setup Done")

	def session_start(self, event):
		self.send_presence()
		self.get_roster()
	
	

	def message(self, msg):		
		if msg['id'] in self.mids :
			return
		print(msg['id'], self.mids)
		if(len(self.mids) > 10):
			self.mids.clear()
		self.mids.append(msg['id'])
		body={}
		try:
			user=str(msg.getFrom()).split('/')[0]
		except Exception as e:
			f=open(logfile, w)
			f.write(e)
			f.close()
		#self.send_message(mto="00507468@indianoil",mbody=user)

		#if msg['type'] in ('chat', 'normal'):
		#	msg.reply("Thanks for sending\n%(body)s" % msg).send()
		
		body['uid']=user.split('@')[0]
		#print(msg,msg['id'])	
		message1=str(msg['body'])
		body['message']=message1
		body['timestamp']=str(time.time())
		a=browser()
		payload=a.dicttoJson(body)
		#print(payload)
		headers={"Content-Type":"application/json"}
		#a.post_request(self.boturl, header=headers, data=message)
		#print("Came here ECHO BOT")
		res=a.post_request(url=boturl, headers=headers, data=payload)
		#print(res)	
	
	def connect_process(self):
		self.connect()
		self.process(block=True)

	def connect_processt(self):
		t1=threading.Thread(target=self.connect_process)
		t1.daemon = True
		t1.start()
	#def send_message(self, url, uid, message):
		

	
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

#boturl="http://127.0.0.1:5001/sendMessage"
#clientID='alexuidian1@jabb.im'
#serverhost="jabb.im"
#clientPass='21101991'
	

if __name__ == "__main__": 
	app.run(host='0.0.0.0', port='5001', debug=True ))
	echobot=EchoBot(clientID, clientPass)
	echobot.boturl=boturl
	echobot.serverhost=serverhost
	echobot.connect_process()
	#t1=threading.Thread(target=echobot.connect_process)
	#t1.start()
