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

import Market
Mkt = Market.MktSliNow()
AddPar = {
	"ExchangeServerHost": "127.0.0.1",
	"ExchangeServerPort": 9501,
	"MaxConnnectTryTime": 100,
	"WaitTimeAfterTryConnect": 2
}
Account=Counter.Account('usr','pwd',AddPar,MktSliNow=Mkt)
Account.ConnectAndLogin()
# SendMsg(s,Msg)
while Account.LogInState==0:
	time.sleep(1)

while 1:
	time.sleep(1)
	x=input(">>>").strip()
	try:
		if x[0]=='p' or x=='P':
			# print(x[1])
			Msg=GetMsg(x[1])
			print(Msg)
			ret,msg,OrderID=Account.PlaceOrder(**Msg)
			print([ret,msg])
		if x[0]=='s' or x=='S':
			Account.SendMsg(Msg)
		if x[0] == 'i' or x == 'I':
			Msg=GetMsg(x[1])
			Account.AccPar['CommissionRate']=Msg['CommissionRate']
			Account.AccPar['Slippage'] =Msg['Slippage'] 
			Account.CashInfo=Msg['CashInfo']
			pos=Msg['000001.SZSE']
			pos.append(Account)
			pos.append({})
			Account.Position['000001.SZSE']=pos
		if x[0]=='o' or x=='O':
			print("======================================================================================")
			print(Account.Order)
			print("======================================================================================")
			print(Account.Position)
			print("======================================================================================")
			print(Account.CashInfo)
			print("======================================================================================")
	except Exception as e:
		print(e)





