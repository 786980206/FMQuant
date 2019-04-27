# -*- coding: utf-8 -*-

import socket
import multiprocessing
import threading
import datetime
import pandas as pd
import json
import time
import uuid
import Market
import GeneralMod
from GeneralMod import ExchangeServerLogger


def GetMsg(X):
	with open('SocketMsg.json') as f:
		Msg=json.load(f)
	return Msg[int(X)]


# 常量定义
POSITION_INDEX=['Code','Vol','VolA','VolFrozen','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
BUFFSIZE=1024 #接收消息缓存区大小，如果以后传的消息多了会修改

# 客户端连接类
class ClientConnection(object):
	def __init__(self,conn,addr,ClientPool):
		self.addr=addr
		self.conn=conn
		self.ClientID=str(uuid.uuid1())
		self.ClientPool=ClientPool

	# 退出
	def Exit(self):
		self.conn.close()
		del self.ClientPool[self.ClientID]
		exit(0)

	# 接收消息
	def RecMsg(self):
		Lock=threading.Lock()
		Msg=''
		while True:
			try:
				RecData=self.conn.recv(BUFFSIZE).decode('utf-8')
				ExchangeServerLogger.debug("读取缓冲区数据:{}".format(RecData))
			except:
				ExchangeServerLogger.warning("接收缓冲区数据失败!")
				self.Exit()
			if RecData=='':self.Exit()
			Msglist,Msg=GeneralMod.AnalyzeMsg(Msg,RecData)
			for AimMsg in Msglist:
				try:
					Lock.acquire()
					self.DealRecMsg(AimMsg)
					Lock.release()
				except Exception as e:
					ExchangeServerLogger.error("处理消息出错:{},{}".format(AimMsg,e))
	# 发送消息
	def SendMsg(self,Msg):
		try:
			Msg=GeneralMod.MakeSendMsg(Msg)
			self.conn.send(str(Msg).encode('utf-8'))
			ExchangeServerLogger.debug("成功发送消息:{}".format(Msg))
			return 1,"发送消息成功"
		except Exception as e:
			ExchangeServerLogger.error("处理消息出错:{}".format(e))
			return 0, "发送消息失败"

	# 处理接收消息的函数
	def DealRecMsg(self,Msg):
		ExchangeServerLogger.debug("处理消息:{}".format(Msg))
		pass
