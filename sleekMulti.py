import csv, sys
import base64
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


# Add sessions dict['authkey']=echobotobject

#boturl='http://10.52.150.150:5007/sendMessage'
port='5007'

	
@app.route("/sendMessage", methods = ['GET', 'POST', 'DELETE'])
#format: Post Method {'client': 'clientid' , 'pass' : 'passwd'  'uid' : 'userid', 'message' : 'message here', 'timestamp:' 'timestamp here'}
def sendMessage():
	message=request.get_json()
	clientID=message['client']
	clientPass=message['pass']
	user=message['uid']
	body=message['message']
	timestamp=str(time.time())
	if 'timestamp' in message.keys():
		timestamp=message['timestamp']
	asyncio.run(send_finally(clientID, clientPass, user+'@'+serverhost, body ))
	return "Hello, World!"

async def send_finally(clientID, clientPass, user, body):
	echobot=app.echobot[clientID]
	await echobot.asend_message(user,body)
	


class EchoBot(ClientXMPP):	
	def __init__(self, jid, password):
		self.conn=ClientXMPP.__init__(self, jid, password, handlefunction=self.message )
		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("ssl_invalid_cert", self.discard)
		self.mids=[]
		print("Setup Done")

	def discard(self, event, cert, direct):
		return
	def session_start(self, event):
		print(self.send_presence())
		print(self.get_roster())

	
	

	def message(self, msg):		
		if msg['id'] in self.mids :
			return
		#print(msg['id'], self.mids)
		if(len(self.mids) > 10):
			self.mids.clear()
		self.mids.append(msg['id'])
		body={}
		try:
			user=str(msg.getFrom()).split('/')[0]
		except Exception as e:
			f=open(logfile, 'a')
			f.write(e)
			f.close()
		#self.send_message(mto="00507468@indianoil",mbody=user)

		#if msg['type'] in ('chat', 'normal'):
		#	msg.reply("Thanks for sending\n%(body)s" % msg).send()
		
		body['uid']=user.split('@')[0]
		#print(msg,msg['id'])	
		message1=str(msg['body'])
		body['message']=message1
		body['pass'] = self.passw
		body['client'] = self.client
		body['timestamp']=str(time.time())
		a=browser()
		payload=a.dicttoJson(body)
		#print(payload)
		headers={"Content-Type":"application/json"}
		#a.post_request(self.boturl, header=headers, data=message)
		#print("Came here ECHO BOT")
		res=a.post_request(url=boturl, headers=headers, data=payload)
		msg.reply(res).send()
	
	def connect_process(self):
		self.connect()
		self.process()
		print("Server Started")

	def connect_processt(self):
		t1=threading.Thread(target=self.connect_process)
		t1.daemon = True
		#print()
		t1.start()
	async def asend_message(self, user, body):
		print(user, body)
		self.send_message(mto=user, mbody=body, mtype='chat')
		#seld.connect()
		#self.process()
	#def send_message(self, url, uid, message):
		

#class Sessions(clientID, clientPass):
#	pass
	# to be added session for all employees
		


if __name__ == "__main__": 
	#for each in member of multidb.csv, create a new echobot with threading.
	f=open('multidb.csv','r')
	c=csv.reader(f)
	app.echobot={} # Dictionary for all bots
	for eachrow in c:
		clientid=eachrow[0]
		serverhost=eachrow[0].split('@')[1]
		clientpass=eachrow[1]
		boturl=eachrow[2]
		echobot=EchoBot(clientid, clientpass)
		echobot.boturl=boturl
		echobot.client=clientid
		echobot.passw=clientpass
		echobot.connect_process()
		app.echobot[clientid]=echobot
		
	#echobot=EchoBot(clientID, clientPass)
	#echobot.boturl=boturl
	#echobot.serverhost=serverhost
	#echobot.connect_process()
	#app.echobot=echobot
	app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False )
	for each in app.echobot.keys():
		echobot=app.echobot[each]
		t1=threading.Thread(target=echobot.connect_process)
		t1.start()


