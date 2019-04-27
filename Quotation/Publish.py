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
	def __init__(self,conn,addr,ExchangeCore,ClientPool):
		self.addr=addr
		self.conn=conn
		self.ExchangeCore=ExchangeCore
		self.ClientID=str(uuid.uuid1())
		self.ClientPool=ClientPool
		self.AccountID=None
		ExchangeServerLogger.info("连接成功:{}".format(self.addr))
	# 退出
	def Exit(self):
		self.conn.close()
		del self.ClientPool[self.ClientID]
		ExchangeServerLogger.info("连接断开:{}".format(self.addr))
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
		Msg=GeneralMod.MakeSendMsg(Msg)
		self.conn.send(str(Msg).encode('utf-8'))
		ExchangeServerLogger.debug("成功发送消息:{}".format(Msg))
		return 1,"发送消息成功"

	# 处理接收消息的函数
	def DealRecMsg(self,Msg):
		ExchangeServerLogger.debug("处理消息:{}".format(Msg))
		# 测试打印字符串
		if Msg['MsgType']=="Print":
			ExchangeServerLogger.debug('处理接收消息的线程打印：{}'.format(Msg))
		# 退出
		if Msg['MsgType']=="Exit":
			self.Exit()
		# 新订单请求
		if Msg['MsgType']=="PlaceOrder":
			OrderID,Order=Msg['OrderID'],Msg['Order']
			self.ExchangeCore.DealNewOrder(OrderID,Order,self)
		# 撤单请求
		if Msg['MsgType']=="CancelOrder":
			OrderID=Msg['OrderID']
			self.ExchangeCore.CancelOrder(OrderID,self)
		# 账户登录
		if Msg['MsgType']=="LogIn":
			self.CheckLogIn(Msg)
		# 账户登出
		if Msg['MsgType']=="LogOut":
			self.Exit()
		# 清除订单池
		if Msg['MsgType']=="Clear":
			self.ExchangeCore.OrderPool=pd.DataFrame(index=ORDER_INDEX)
			ExchangeServerLogger.debug("清除ExchangeCore.OrderPool成功")
	# 登录检查
	def CheckLogIn(self,Msg):
		ExchangeServerLogger.info("客户端登录:{}".format(Msg))
		if self.CheckUsr(Msg["Usr"],Msg["Pwd"]):
			self.AccountID=Msg['AccountID']
			Msg={'MsgType':'LogInReturn','ret':1,'msg':'登录成功','session':'XXXXXXX'}
			ExchangeServerLogger.info("发送登录回执:{}".format(Msg))
			self.SendMsg(Msg)
	# 用户信息检查
	def CheckUsr(self,Usr,Pwd):
		ExchangeServerLogger.debug("验证用户身份:{},{}".format(Usr,Pwd))
		return 1


# 初始化
def Init():
	ExchangeServerSetting=GeneralMod.LoadJsonFile(GeneralMod.PathJoin(GeneralMod.BASE_SETTING_FILE))["ExchangeServerSetting"]
	ExchangeCore=Exchange()
	ExchangeServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ExchangeServer.bind((ExchangeServerSetting["ExchangeServerHost"],ExchangeServerSetting["ExchangeServerPort"]))
	ExchangeServer.listen(ExchangeServerSetting["ExchangeServerListenLimit"])
	ClientPool={}
	ExchangeServerLogger.info("启动成功:ExchangeServer")
	while True:
		ExchangeServerLogger.debug("等待新连接:ExchangeServer")
		conn,addr=ExchangeServer.accept()
		Client=ClientConnection(conn,addr,ExchangeCore,ClientPool)
		ClientPool[Client.ClientID]=Client
		# ClientThread=multiprocessing.Process(name="ClientThread({})".format(Client.ClientID),target=Client.RecMsg)
		ClientThread = threading.Thread(name="ClientThread({})".format(Client.ClientID), target=Client.RecMsg)
		# 子线程为守护线程
		ClientThread.daemon=True
		ClientThread.start()
		ExchangeServerLogger.debug("客户端({})已连接，消息接收线程启动成功".format(Client.ClientID))
		# # 等待客户端登录
		# time.sleep(ExchangeServerSetting["ClientLogInTimeLimit"])
		# # 如果没有在指定时间内登录，那么结束掉客户端连接
		# if Client.AccountID==None:Client.Exit()
		# 用于调试===============================================================
		# while 1:
		# 	# from SocketCliTest import GetMsg
		# 	time.sleep(1)
		# 	x = input(">>>").strip()
		# 	try:
		# 		if x[0] == 's' or x == 'S':
		# 			Msg = GetMsg(x[1])
		# 			# print(Msg)
		# 			ExchangeCore.SendMsg(Client,Msg)
		# 	except Exception as e:
		# 		print(e)
		# 用于调试===============================================================

################################################ 类定义 ###############################################################
class Exchange(object):
	# 初始化
	def __init__(self,MktSliNow=None,OrderPool=None):
		self.OrderPool=OrderPool if OrderPool!=None else pd.DataFrame(index=ORDER_INDEX)
		self.MktSliNow=MktSliNow if MktSliNow!=None else Market.MktSliNow()
		self.Slippage=0

	# 向客户端发送消息
	def SendMsg(self,Client,Msg):
		ExchangeServerLogger.debug("发送消息:{}".format(Msg))
		Client.SendMsg(Msg)

	# 报单回报
	def SendOrderReturn(self,OrderID,Client,ret,msg):
		if ret==1:
			OrderTime=self.OrderPool[OrderID][7]
		else:
			OrderTime=self.CreateOrderTime()
		Msg={
			'MsgType':'OrderReturn',
			'OrderID':OrderID,
			'ret':ret,
			'msg':msg,
			'OrderTime':OrderTime
		}
		ExchangeServerLogger.info("发送报单回执:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# 成交回报
	def SendTransactionReturn(self,OrderID,Client,MatchInfo,OrderState,MatchTime):
		Msg={
			'MsgType':'TransactionReturn',
			'OrderID':OrderID,
			'MatchInfo':MatchInfo,
			'OrderState':OrderState,
			'MatchTime':MatchTime
		}
		ExchangeServerLogger.info("发送成交回执:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# 撤单回报
	def SendCancelOrderReturn(self,Client,OrderID,ret,msg,CancelTime):
		Msg={
			'MsgType':'CancelOrderReturn',
			'OrderID':OrderID,
			'ret':ret,
			'msg':msg,
			'CancelTime':CancelTime
		}
		ExchangeServerLogger.info("发送撤单回执:{}".format(Msg))
		self.SendMsg(Client, Msg)

	# 获取订单数据
	def GetOrderByID(self,OrderID,Item=ORDER_INDEX):
		if type(Item) is not list:Item=[Item]
		if OrderID in self.OrderPool.columns:
			return list(self.OrderPool[OrderID].loc[Item])
		else:
			return [None]*len(self.OrderPool.columns)

	# 生成撮合成交时间
	def CreateMatchTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 生成撤单时间
	def CreateCancelTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 判断订单状态（如订单全部成交则需要取消等）
	def CheckOrderByID(self,OrderID):
		ExchangeServerLogger.debug("检查订单状态:{}".format(OrderID))
		# 订单数据
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=self.GetOrderByID(OrderID)
		# 判断是否全部成交
		if Volume==VolumeMatched and State=='AllMatched':
			# 清除订单
			ret,msg=self.DelOrderByID(OrderID)
		else:
			ret,msg=1,"订单正常"
		return ret,msg

	# 删除订单
	def DelOrderByID(self,OrderID):
		ExchangeServerLogger.info("删除订单:{}".format(OrderID))
		if OrderID not in self.OrderPool:
			return 0,'删除订单失败，订单不存在'
		self.OrderPool.drop(labels=OrderID, axis=1, inplace=True)
		return 1,'删除订单成功'

	# 生成订单下单时间
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 检查新订单
	def CheckNewOrder(self,OrderID,Order,Client):
		ExchangeServerLogger.debug("检查新报单:{},{}".format(OrderID, Order))
		if OrderID in self.OrderPool:
			ret,msg=0, '订单编码重复'
			return ret,msg
		if Client.AccountID==None:
			return 0,'账户ID异常'
		ret,msg=self.LogNewOrder(OrderID,Order,Client)
		return ret,msg

	# 记录新订单，将新订单加入订单记录中并生成订单id
	def LogNewOrder(self,OrderID,Order,Client):
		ExchangeServerLogger.info("记录新报单:{},{}".format(OrderID,Order))
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# 记录订单
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,0,'WaitToMatch',0,self.CreateOrderTime(),OrderID,'Mkt',Client,AddPar]
		return 1,'下单成功'

	# 处理从柜台新推过来的订单数据
	def DealNewOrder(self,OrderID,Order,Client,MarkeSliNow=None):
		ExchangeServerLogger.info("处理新报单:{},{}".format(OrderID,Order))
		# 检查新订单
		ret,msg=self.CheckNewOrder(OrderID,Order,Client)
		ExchangeServerLogger.debug("检查报单结果:{},{}".format(ret,msg))
		# 发送订单回报
		self.SendOrderReturn(OrderID,Client,ret,msg)
		# ExchangeServerLogger.debug("发送订单回报结果:{},{}".format(ret, msg))
		# 检查不通过则退出
		if ret==0:return
		# 开始撮合
		ret,msg=self.MatchOrderByID(OrderID)
		return ret,msg

	# 处理撮合结果
	def DealMatchRetInOrderPool(self,OrderID,MatchInfo):
		ExchangeServerLogger.debug("OrderPool处理撮合结果:{},{}".format(OrderID,MatchInfo))
		# 订单数据
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 开始处理
		# 计算新的订单记录的字段
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old
		# 已成交量
		VolumeMatched=VolumeMatched_Old+VolumeMatching
		# 状态
		# 如果已成=订单量
		if VolumeMatched==Volume_Old:
			State='AllMatched'
		elif VolumeMatched<Volume_Old and VolumeMatched!=0:
			State='PartMatched'
		else:
			State='WaitToMatch'
		# 回写数据到OrderPool
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config]
		# 检查订单状态（如订单全部成交则需要删除等）
		ret,msg=self.CheckOrderByID(OrderID)
		ExchangeServerLogger.debug("检查订单结果:{},{}".format(ret, msg))
		return 1,State

	# 仿真撮合订单的函数
	# 需要用到订单数据，市场数据，柜台数据（费率等），其他撮合数据（如滑点，最大成交比例等）
	def MatchSimulation(self,OrderID,MktInfo):
		ExchangeServerLogger.debug("仿真撮合:{},{}".format(OrderID,MktInfo))
		# 订单数据
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=self.GetOrderByID(OrderID)
		# 市场数据
		Price4Trd=MktInfo['Price4Trd']
		Volume4Trd=MktInfo['Volume4Trd']
		# 撮合设置数据
		Slippage=self.Slippage
		# 计算订单未成交量
		VolumeNotMatched=Volume-VolumeMatched
		# 开始撮合
		# 价格对比
		# 市价多单
		if Price==0 and Direction==1:
			PriceMatching=Price4Trd+Slippage
		# 限价多单
		elif (Price>=Price4Trd) and Direction==1:
			PriceMatching=Price4Trd
		# 市价平多
		elif Price==0 and Direction==0:
			PriceMatching=Price4Trd-Slippage
		# 限价平多
		elif Price<=Price4Trd and Direction==0:
			PriceMatching=Price4Trd
		else:
			return 0,'价格不合适，未能成交',{'PriceMatching':0,'VolumeMatching':0}
		# 成交量比对
		# 全部成交
		if VolumeNotMatched<=Volume4Trd:
			VolumeMatching=VolumeNotMatched
		# 部分成交
		elif VolumeNotMatched>Volume4Trd:
			VolumeMatching=Volume4Trd
		else:
			return 0,'成交量比对时出错！',{'PriceMatching':0,'VolumeMatching':0}
		return 1,'',{'PriceMatching':PriceMatching,'VolumeMatching':VolumeMatching}

	# 撮合订单以及处理撮合结果
	def MatchOrderByID(self,OrderID):
		ExchangeServerLogger.info("撮合订单:{}".format(OrderID))
		# 获取订单标的代码和柜台客户端
		Code,Client=self.GetOrderByID(OrderID,['Code','Account'])
		MktInfo = {'Price4Trd': self.MktSliNow.GetDataByCode(Code, 'Price'),
				   'Volume4Trd': self.MktSliNow.GetDataByCode(Code, 'Volume4Trd')}
		ret, msg, MatchInfo = self.MatchSimulation(OrderID, MktInfo)
		# 判断是否成交
		if MatchInfo['VolumeMatching'] == 0:
			return 1, '无成交'
		# 处理撮合结果
		# OrderPool更新
		ret,OrderState = self.DealMatchRetInOrderPool(OrderID, MatchInfo)
		ExchangeServerLogger.debug("OrderPool更新:{},{},{}".format(OrderID,ret, OrderState))
		# 市场行情切片也要处理撮合结果（扣除成交量等）
		self.MktSliNow.DealMatchRet(Code, MatchInfo)
		# 生成成交时间
		MatchTime = self.CreateMatchTime()
		# 通知柜台处理成交回报
		self.SendTransactionReturn(OrderID, Client, MatchInfo, OrderState, MatchTime)
		return 1,''

	# 撤单函数
	def CancelOrder(self,OrderID,Client):
		ExchangeServerLogger.info("撤销订单:{}".format(OrderID))
		# 生成撤单时间
		CancelTime=self.CreateCancelTime()
		# 检查撤单是否有效
		ret,msg=self.CheckCancelOrder(OrderID,Client)
		ExchangeServerLogger.debug("检查撤单是否有效:{},{}".format(ret,msg))
		if ret==0:
			self.SendCancelOrderReturn(Client,OrderID,ret,msg,CancelTime)
			return 0,'撤单失败'
		# 删除订单
		ret,msg=self.DelOrderByID(OrderID)
		if ret==1:
			msg='撤单成功'
		# 发送撤单回报
		self.SendCancelOrderReturn(Client,OrderID,ret,msg,CancelTime)

	# 检查撤单信息
	def CheckCancelOrder(self,OrderID,Client):
		if Client.AccountID==None:
			return 0,'账户ID异常'
		if OrderID not in self.OrderPool:
			return 0,'无效订单编码'
		return 1,'检查撤单成功'

	# 获取订单ID列表
	def GetOrderIDList(self):
		return list(self.OrderPool.columns)

	# 新行情来了，要逐订单开始撮合
	def OnNewQuoteComing(self):
		ExchangeServerLogger.debug("新行情来了,逐订单开始撮合")
		# 获取订单列表
		OrderIDList=self.GetOrderIDList()
		# 开始逐订单撮合
		for OrderID in OrderIDList:
			self.MatchOrderByID(OrderID)



if __name__=='__main__':
	Init()