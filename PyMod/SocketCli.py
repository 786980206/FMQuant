# -*- coding: utf-8 -*-

import socket
import multiprocessing
import datetime
import pandas as pd
import json
import time
import json
import Counter
import Market

def GetMsg(X):
	with open('SocketMsg.json') as f:
		Msg=json.load(f)
	return Msg[int(X)]

def SendMsg(server,Msg):
	if type(Msg) is dict:Msg=json.dumps(Msg)
	Msg="Msg:"+Msg+"|End"
	print(Msg)
	server.send(Msg.encode('utf-8'))

ConnectionClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ConnectionClient.connect(("127.0.0.1",9502))
while 1:
	time.sleep(1)
	x=input(">>>").strip()
	try:
		Msg=str(x)
		if Msg=="q":Msg={"MsgType":"Sub","QuoteType":"k_StsPerTick","Par":[["AU1906.SHFE"]]}
		SendMsg(ConnectionClient,Msg)
	except Exception as e:
		print(e)





