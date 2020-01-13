import sys
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as soup
from datetime import datetime
from http.cookiejar import CookieJar
import json
import ssl
import pdb
import websocket
import threading
import time

class browser:
	cj=CookieJar()
	def myurlopen(self, request):
		response=""
		try:
			ssl._create_default_https_context = ssl._create_unverified_context
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
			#pdb.set_trace()
			response=opener.open(request)
		except urllib.error.URLError as e:
			if hasattr(e, 'reason'):
				print(request.full_url, 'We failed to reach a server.')
				print(('Reason: ', e.reason))
				response=(0,e.reason)
				return response
			elif hasattr(e, 'code'):
				print('The server could not fulfill the request.')
				print(('Error code: ', e.code))
				response=(0,e.code)
				return response
			else:
	    			# everything is fine
				pass
		return (1,response.read().decode())
	
	def get_request(self, url):
		request = urllib.request.Request(url)
		res= self.myurlopen(request)
		if(res[0]):	
			return res[1]
		else:
			return ""
	
	def post_request(self, url, headers, data):
		req = urllib.request.Request(url, data.encode("utf-8"))
		req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 8.0.0; ONEPLUS A3003 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36')
		for each in list(headers.keys()):
			req.add_header(each, headers[each])
		res=self.myurlopen(req)
		if(res[0]):	
			return res[1]
		else:
			return ""
	
	def encode_string(self, string):
		if int(sys.version[0]) < 3:
			encoderfun=urllib.quote_plus
		else:
			encoderfun=urllib.parse.quote_plus		
		return encoderfun(string)
	
	def TextFromID(self,html,ID):
		#pdb.set_trace()
		try:
			bs=soup(html, features="lxml")
		except Exception as e:
			print(e)
		#print(bs.findAll(id=ID))
		return bs.findAll(id=ID)[0].text

	def jsontoDict(self,jsondata):
		return json.loads(jsondata)
	def dicttoJson(self,dict1):
		return json.dumps(dict1)
	
	def gettimestamp(self):
		timestamp=datetime.now()
		return timestamp.strftime("%Y-%m-%dT%H:%M:%S") + "." + timestamp.strftime("%s")[0:3]+"Z"
	
########### *** WEBSOCKETS *** #############################################
	def ws_on_message(self, ws, message):
		print(message)

	def ws_on_error(self, ws, error):
		print(error)

	def ws_on_close(self, ws):
		self.ws_open=False
		print("### One Websocket closed ###")

	def ws_on_open(self, ws):
		self.ws_open=True
		def run(*args):
			while ('1' == '1' ):
				time.sleep(1)
				if self.ws_open == False :
					ws.close()
					break
		opent=threading.Thread(target=run)
		opent.daemon= True
		opent.start()
		#ws.send("Hello")
		if self.ws_open == True:
			print("### One Websocket Opened ###")
		else:
			print("### Could not Open Websocket for a user ###")
		return(0)

	def ws_start(self, url, on_open=None, on_message=None, on_error=None, on_close = None, trace=True):
#		websocket.enableTrace(trace)
		if on_open == None:
			on_open=self.ws_on_open
		if on_message == None:
			on_message=self.ws_on_message
		if on_error == None:
			on_error=self.ws_on_error
		if on_close == None:
			on_close = self.ws_on_close
	#def ws_start(self, url ):
		self.ws = websocket.WebSocketApp(url,
			on_message = lambda ws, message: on_message(ws, message),
			on_error =  lambda ws, error : on_error(ws, error),
			on_close = lambda ws : on_close(ws)
		)
		self.ws.on_open = lambda ws : on_open(ws)
		#self.ws.run_forever(sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
		wst = threading.Thread(target=self.ws.run_forever, kwargs= { 'sslopt' : {"check_hostname": False, "cert_reqs": ssl.CERT_NONE} , })
		wst.daemon = True
		wst.start()
		time.sleep(1)
