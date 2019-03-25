# -*- coding: utf-8 -*-

import socket
import multiprocessing
import datetime
import pandas as pd
import json
import time
import json

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',9501))
while True:
	Msg={"MsgType":"DealNewOrder",
		 "Order":{'Code':'000001.SZSE','Direction':0,'Price':100,'Volume':200,'AddPar':{}},
		 "AccountID":"1200000000",
		 }
	Msg=json.dumps(Msg)
	Msg="Msg:"+Msg+"|End"
	s.send(Msg.encode("utf-8"))
	Msg=input(">>>").strip()
	Msg="Msg:" + Msg + "|End"
	s.send(Msg.encode('utf-8'))