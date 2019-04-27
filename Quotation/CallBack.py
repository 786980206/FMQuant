# -*- coding: UTF-8 -*-

__author__="WindSing"

import os,sys
sys.path.append('lib')
import time
import win32api,win32con
from QtAPI import *
from QtDataAPI import *
import pandas as pd
from GeneralMod import GuiLogger
import


# 回调对象
class Quote(object):
	# 初始化
	def __init__(self,Usr="nblfm_qt",Pwd="199568"):
		self.Usr=Usr
		self.Pwd=Pwd
		self.ConnectPool=[]
		self.DataMap={}
		self.DataMap["k_StsPerTick"]=pd.DataFrame(index=["Symbol","TradingTime","BuyPrice","BuyVol","SellPrice","SellVol","RecTime"])

		ExchangeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ExchangeServer.bind((ExchangeServerSetting["ExchangeServerHost"], ExchangeServerSetting["ExchangeServerPort"]))
		ExchangeServer.listen(ExchangeServerSetting["ExchangeServerListenLimit"])
		ClientPool = {}
		ExchangeServerLogger.info("启动成功:ExchangeServer")
		while True:
			ExchangeServerLogger.debug("等待新连接:ExchangeServer")
			conn, addr = ExchangeServer.accept()
			Client = ClientConnection(conn, addr, ExchangeCore, ClientPool)
			ClientPool[Client.ClientID] = Client
			# ClientThread=multiprocessing.Process(name="ClientThread({})".format(Client.ClientID),target=Client.RecMsg)
			ClientThread = threading.Thread(name="ClientThread({})".format(Client.ClientID), target=Client.RecMsg)
			# 子线程为守护线程
			ClientThread.daemon = True
			ClientThread.start()
			ExchangeServerLogger.debug("客户端({})已连接，消息接收线程启动成功".format(Client.ClientID))

	# 登录
	def Login(self):
		ret, errMsg = QtLogin(self.Usr,self.Pwd)

	# 登出
	def Logout(self):
		ret, errMsg = QtLogout(self.Usr)

	# A.订阅k_Sts
	def Sub_k_StsPerTick(SubCB, Code):
		RegSubStsPerTickCB(SubCB.OnSubSts)
		ret, errMsg = Subscribe(EQuoteData["k_StsPerTick"], 60, Code, [])


	# 分时数据回调
	def OnSubSts(self,data):
		# 构造数据
		Code = "{}.{}".format(data.Symbol, data.Market)
		TradingTime = str(data.TradingTime)
		BuyPrice = list(data.BuyPrice)
		BuyVolume = list(data.BuyVolume)
		SellPrice = list(data.SellPrice)
		SellVolume = list(data.SellVolume)
		ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
		RecTime = time.strftime(ISOTIMEFORMAT, time.localtime())
		Data = [Code, TradingTime, BuyPrice, BuyVolume, SellPrice, SellVolume, RecTime]
		print(Data)
		# 存储数据
		self.SaveData("k_StsPerTick",Data)
		# 推送数据


	# 储存数据
	def SaveData(self,Type,Data):
		try:
			Index=Data[0]
			self.DataMap[Type][Index]=Data
		except Exception as e:
			print(e)
