import os,sys
sys.path.append('lib')
import time
import datetime
from QtAPI import *
from QtDataAPI import *
import pandas as pd
import numpy as np
from multiprocessing import Queue
from GeneralMod import GuiLogger
import threading
import socket
import SocketServerConnection
Lock=threading.Lock()

class data(object):
	count=0
	def __init__(self):
		print("我被调用了？")
		self.count=self.count+1
		self.Symbol = "000001"
		self.Market = "SZSE"
		self.TradingTime = datetime.datetime.now()
		self.BuyPrice = np.random.randint(10, 15, 5).tolist()
		self.BuyVolume = (np.random.randint(10, 20, 5) * 100).tolist()
		self.SellPrice = np.random.randint(15, 20, 5).tolist()
		self.SellVolume = (np.random.randint(10, 20, 5) * 100).tolist()



# 回调对象
class Quote(object):
	# 初始化
	def __init__(self,Usr="nblfm_qt",Pwd="199568",Host="127.0.0.1",Port=9502,ServerListenLimit=5):
		self.a=2
		# 基础信息
		self.Usr=Usr
		self.Pwd=Pwd
		# 连接信息
		self.Host=Host
		self.Port=Port
		self.ServerListenLimit=ServerListenLimit
		self.ClientPool={}
		# 数据信息
		self.DataMap={}
		self.DataMap["k_StsPerTick"]=pd.DataFrame(index=["Symbol","TradingTime","BuyPrice","BuyVol","SellPrice","SellVol","RecTime"])
		# 回调相关
		self.NeedPublish=False
		# 线程信息
		# 1.主线程：将会开启Socket服务，等待客户端连接
		# 2.回调线程：由订阅启动，目标会处理订阅接收信息
		# 3.推送线程：接收到的订阅会分发给连接上的客户端
		# 4.客户端消息监听线程：将会在客户端连接上时启动，接收客户端消息
		self.PublishThread=threading.Thread(target=self.PublishMain)
		self.PublishThread.daemon=True
		self.PublishThread.start()
		# 启动Socket服务
		self.Server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Server.bind((self.Host,self.Port))
		self.Server.listen(self.ServerListenLimit)
		GuiLogger.info("启动成功:ExchangeServer")
		# 登录QTAPI
		# self.Login()

		# 开始等待连接
		while True:
			GuiLogger.debug("等待新连接:ExchangeServer")
			conn, addr = self.Server.accept()
			Client = SocketServerConnection.ClientConnection(conn, addr, self.ClientPool)
			self.ClientPool[Client.ClientID] = Client
			# 重写消息接收函数
			Client.DealRecMsg=self.DealClientMsg
			ClientThread = threading.Thread(name="ClientThread({})".format(Client.ClientID), target=Client.RecMsg)
			# 子线程为守护线程
			ClientThread.daemon = True
			ClientThread.start()
			GuiLogger.debug("客户端({})已连接，消息接收线程启动成功".format(Client.ClientID))
			# 测试用：开始推数据
			while 1:
				Data=data()
				self.OnSubSts(Data)
				time.sleep(3)

	# 处理客户端消息
	def DealClientMsg(self,Msg):
		GuiLogger.debug("处理消息:{}".format(Msg))
		if Msg["MsgType"]=="Sub":
			self.Sub(Msg["QuoteType"],Msg["Par"])

	# 登录
	def Login(self):
		ret, errMsg = QtLogin(self.Usr,self.Pwd)

	# 登出
	def Logout(self):
		ret, errMsg = QtLogout(self.Usr)

	# 行情订阅
	def Sub(self,QuoteType,Par):
		GuiLogger.debug("开始订阅:{},{}".format(QuoteType,Par))
		try:
			if QuoteType=="k_StsPerTick":
				ret,msg=self.Sub_k_StsPerTick(*Par)
				GuiLogger.info("订阅成功:{},{}".format(QuoteType,Par))
		except Exception as e:
			GuiLogger.error(e)

	# 订阅k_Sts
	def Sub_k_StsPerTick(SubCB, Code):
		RegSubStsPerTickCB(SubCB.OnSubSts)
		ret, errMsg = Subscribe(EQuoteData["k_StsPerTick"], 60, Code, [])
		ret=1 if ret==0 else 0
		return ret,errMsg

	# 推送主线程线程
	def PublishMain(self):
		while 1:
			Lock.acquire()
			if self.NeedPublish:
				self.Publish()
			Lock.release()
			# print("我在运行")

	# 推送消息的函数
	def Publish(self):
		for Client in self.ClientPool.values():
			Msg=self.DataMap["k_StsPerTick"].to_dict()
			print(Msg)
			Client.SendMsg(Msg)
		# GuiLogger.debug("接收到分发消息的命令")


	# 分时数据回调
	def OnSubSts(self,data):
		Lock.acquire()
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
		self.NeedPublish=True
		Lock.release()


	# 储存数据
	def SaveData(self,Type,Data):
		try:
			Index=Data[0]
			self.DataMap[Type][Index]=Data
		except Exception as e:
			print(e)


if __name__=='__main__':
	Quotation=Quote()
	Quotation.Login()
	Quotation.Sub_k_StsPerTick(["*.SHFE"])
	while 1:
		time.sleep(2)
		GuiLogger.info("主线程:{}".format(Quotation.a))
		Quotation.a+=2