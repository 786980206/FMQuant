# -*- coding: utf-8 -*-
import os,sys
sys.path.append("..\\")
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
import DataServer.QOperation as Q
import Common as cm
import DataDef as DataDef

# 客户端连接类
class ClientConnection(object):
	def __init__(self,conn,addr:str,ExchangeCore,ClientPool:{},Q:Q.Q)->None:
		self.addr=addr
		self.conn=conn
		self.ExchangeCore=ExchangeCore
		self.ClientID=uuid.uuid1()
		self.ClientPool=ClientPool
		self.AccountID=None
		ExchangeServerLogger.info("连接成功:{}".format(self.addr))
		self.Q=Q
		self.ConnectInfoTable="Exchange_ConnectInfo"

	# 退出
	def Exit(self)->None:
		self.conn.close()
		del self.ClientPool[self.ClientID]
		self.Q.Del(self.ConnectInfoTable,'ClientID="G"$("{}")'.format(self.ClientID))
		ExchangeServerLogger.info("连接断开:{}".format(self.addr))
		exit(0)

	# 接收消息
	def RecMsg(self):
		Lock=threading.Lock()
		Msg=''
		while True:
			try:
				RecData=self.conn.recv(DataDef.BUFFSIZE).decode('utf-8')
				ExchangeServerLogger.debug("读取缓冲区数据:{}".format(RecData))
			except:
				ExchangeServerLogger.warning("接收缓冲区数据失败!")
				self.Exit()
			if RecData=='':self.Exit()
			Msglist,Msg=GeneralMod.AnalyzeMsg(Msg,RecData)
			for AimMsg in Msglist:
				try:
					with Lock:
						self.DealRecMsg(AimMsg)
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
			OrderID,Order=uuid.UUID(Msg['OrderID']),Msg['Order']
			self.ExchangeCore.DealNewOrder(OrderID,Order,self)
		# 撤单请求
		if Msg['MsgType']=="CancelOrder":
			OrderID=uuid.UUID(Msg['OrderID'])
			self.ExchangeCore.CancelOrder(OrderID,self)
		# 账户登录
		if Msg['MsgType']=="LogIn":
			self.CheckLogIn(Msg)
		# 账户登出
		if Msg['MsgType']=="LogOut":
			self.Exit()
		# 清除订单池
		if Msg['MsgType']=="Clear":
			[self.ExchangeCore.DelOrderByID(x) for x in self.ExchangeCore.GetOrderList()]
			ExchangeServerLogger.debug("清除ExchangeCore.OrderPool成功")

	# 登录检查
	def CheckLogIn(self,Msg):
		ExchangeServerLogger.info("客户端登录:{}".format(Msg))
		if self.CheckUsr(Msg["Usr"],Msg["Pwd"]):
			self.AccountID=self.MakeAccountID(Msg["Usr"])
			LogInTime=self.CreateTime()
			ValueList={
				"ClientID":[self.ClientID],
				"Usr":[Msg["Usr"]],
				"AccountID":[self.AccountID],
				"ConnectState":[1],
				"Addr":[self.addr],
				"ConnectTime":[LogInTime]
			}
			self.Q.Insert(self.ConnectInfoTable,ValueList)
			Msg={'MsgType':'LogInReturn','ret':1,'msg':'登录成功','session':'XXXXXXX','AccountID':str(self.AccountID)}
			ExchangeServerLogger.info("发送登录回执:{}".format(Msg))
			self.SendMsg(Msg)

	# 生成AccountID
	def MakeAccountID(self,Usr:str)->uuid.UUID:
		return uuid.uuid3(DataDef.NAMESPACE_ACCOUNTID,Usr)

	# 用户信息检查
	def CheckUsr(self,Usr,Pwd):
		ExchangeServerLogger.debug("验证用户身份:{},{}".format(Usr,Pwd))
		return 1

	# 生成登录时间
	def CreateTime(self)->str:
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

# 初始化
def Init():
	ExchangeServerSetting=GeneralMod.LoadJsonFile(GeneralMod.PathJoin(GeneralMod.BASE_SETTING_FILE))["ExchangeServerSetting"]
	# 初始化KDB操作对象
	# 初始化连接池
	ClientPool = {}
	# 初始化交易所对象
	ExchangeCore=Exchange(DataDef.DataOperationObject,ClientPool)
	# 初始化服务连接监听对象
	ExchangeServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ExchangeServer.bind((ExchangeServerSetting["ExchangeServerHost"],ExchangeServerSetting["ExchangeServerPort"]))
	ExchangeServer.listen(ExchangeServerSetting["ExchangeServerListenLimit"])
	ExchangeServerLogger.info("启动成功:ExchangeServer")
	# 开始监听
	while True:
		ExchangeServerLogger.debug("等待新连接:ExchangeServer")
		conn,addr=ExchangeServer.accept()
		Client=ClientConnection(conn,addr,ExchangeCore,ClientPool,DataDef.DataOperationObject)
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
# ExchangeBase：交易所基类，只提供与Client的交互和其他基础方法
class ExchangeBase(object):
	# 初始化
	def __init__(self,DateaOperationObject,ClientPool:dict,MktSliNow=None):
		self.MktSliNow=MktSliNow if MktSliNow!=None else Market.MktSliNow()
		self.Slippage=0
		# kdb连接信息
		self.ORDER_INDEX = DataDef.ORDER_INDEX
		self.Q=DateaOperationObject
		self.OrderPoolTable="Exchange_OrderPool"
		# 连接池信息
		self.ConnectInfoTable="Exchange_ConnectInfo"
		self.ClientPool=ClientPool
		# 清空连接池
		self.ClearConnectInfo()
		# 清空订单池
		self.ClearOrderPool()

	# 清空连接池
	def ClearConnectInfo(self):
		self.Q.Del(self.ConnectInfoTable)

	# 清空订单池
	def ClearOrderPool(self):
		self.Q.Del(self.OrderPoolTable)

	# 向客户端发送消息
	def SendMsg(self, Client:ClientConnection, Msg:str):
		ExchangeServerLogger.debug("发送消息:{}".format(Msg))
		Client.SendMsg(Msg)

	# 通过AccountID来找到客户端连接
	def GetClientByAccountID(self,AccountID:uuid.UUID)->ClientConnection:
		pd_ret=self.Q.Query(self.ConnectInfoTable,["ClientID"],'AccountID="G"$("{}")'.format(AccountID))
		ret=list(pd_ret["ClientID"])
		ClientList=[self.ClientPool[x] for x in ret]
		ExchangeServerLogger.debug("获取到{}对应的{}个客户端连接".format(AccountID,len(ClientList)))
		return ClientList

	# 生成订单下单时间
	def CreateOrderTime(self)->str:
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 生成撮合成交时间
	def CreateMatchTime(self)->str:
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 生成撤单时间
	def CreateCancelTime(self)->str:
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 获取订单ID列表
	def GetOrderIDList(self)->[uuid.UUID]:
		pd_ret=self.Q.Query(self.OrderPoolTable,["OrderID"])
		ret=list(pd_ret["OrderID"])
		return ret

	# 获取订单数据
	def GetOrderByID(self,OrderID:uuid.UUID,Field:list=DataDef.ORDER_INDEX)->list:
		if OrderID in self.GetOrderIDList():
			# 从kdb+获取数据
			pd_ret = self.Q.Query(self.OrderPoolTable,Field,'OrderID="G"$("{}")'.format(OrderID))
			ret=list(pd_ret.iloc[0])
			return ret
		else:
			return [None] * len(Field)

	# 删除订单
	def DelOrderByID(self,OrderID:uuid.UUID)->[int,str]:
		ExchangeServerLogger.info("删除订单:{}".format(OrderID))
		if OrderID not in self.GetOrderIDList():
			return 0, '删除订单失败，订单不存在'
		self.Q.Del(self.OrderPoolTable, 'OrderID="G"$("{}")'.format(OrderID))
		return 1, '删除订单成功'

	# 记录新订单，将新订单加入订单记录中并生成订单id
	def AddOrder(self,OrderID:uuid.UUID,Order:dict,Client:ClientConnection)->[int,str]:
		ExchangeServerLogger.info("记录新报单:{},{}".format(OrderID,Order))
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		AccountID=Client.AccountID
		# 记录订单
		self.Q.Insert(self.OrderPoolTable,{
			"OrderID": [OrderID],
			"Code": [Code],
			"Direction": [Direction],
			"Price": [Price],
			"Volume": [Volume],
			"VolumeMatched":[0],
			"State": ['WaitToMatch'],
			"AvgMatchingPrice":[0],
			"OrderTime": [self.CreateOrderTime()],
			"Mkt": [cm.GetExchangeByCode(Code)],
			"AccountID": [AccountID],
			"AddPar": [AddPar]
		})
		return 1,'下单成功'

	# 修改订单内容
	def UpdateOrderByID(self,OrderID:uuid.UUID,ValueDict:dict)->[int,str]:
		if "AddPar" in ValueDict:ValueDict["AddPar"]=GeneralMod.ToStr(ValueDict["AddPar"])
		self.Q.Update(self.OrderPoolTable,ValueDict,'OrderID="G"$("{}")'.format(OrderID))

	# 判断订单状态（如订单全部成交则需要取消等）
	def CheckOrderByID(self,OrderID:uuid.UUID)->[int,str]:
		ExchangeServerLogger.debug("检查订单状态:{}".format(OrderID))
		# 订单数据
		AccountID,OrderID,Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,Mkt,AddPar=self.GetOrderByID(OrderID)
		if OrderID==None:
			return 0,"订单不存在"
		# 判断是否全部成交
		elif Volume==VolumeMatched and State=='AllMatched':
			# 清除订单
			ret,msg=self.DelOrderByID(OrderID)
		else:
			ret,msg=1,"订单正常"
		return ret,msg

	# 发送下单单回报
	def SendOrderReturn(self,OrderID:uuid.UUID,Client:ClientConnection,ret:int,msg:str)->None:
		if ret==1:
			OrderTime=self.GetOrderByID(OrderID,["OrderTime"])[0]
		else:
			OrderTime=self.CreateOrderTime()
		Msg={
			'MsgType':'OrderReturn',
			'OrderID':str(OrderID),
			'ret':ret,
			'msg':msg,
			'OrderTime':OrderTime
		}
		ExchangeServerLogger.info("发送报单回执:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# 发送成交回报
	def SendTransactionReturn(self,OrderID:uuid.UUID,Client:ClientConnection,MatchInfo:dict,OrderState:str,MatchTime:str)->None:
		Msg={
			'MsgType':'TransactionReturn',
			'OrderID':str(OrderID),
			'MatchInfo':MatchInfo,
			'OrderState':OrderState,
			'MatchTime':MatchTime
		}
		ExchangeServerLogger.info("发送成交回执:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# 发送撤单回报
	def SendCancelOrderReturn(self,OrderID:uuid.UUID,Client:ClientConnection,ret:int,msg:str,CancelTime:str)->None:
		Msg={
			'MsgType':'CancelOrderReturn',
			'OrderID':str(OrderID),
			'ret':ret,
			'msg':msg,
			'CancelTime':CancelTime
		}
		ExchangeServerLogger.info("发送撤单回执:{}".format(Msg))
		self.SendMsg(Client, Msg)

	# 检查新订单
	def CheckNewOrder(self,OrderID:uuid.UUID,Order:dict,Client:ClientConnection)->[int,str]:
		ExchangeServerLogger.debug("检查新报单:{},{}".format(OrderID, Order))
		if OrderID in self.GetOrderIDList():
			ret,msg=0, '订单编码重复'
			return ret,msg
		if self.CheckAccount(Client)==0:
			return 0,'账户ID异常'
		return 1,"订单有效"

	# 检查账户信息
	def CheckAccount(self,Client:ClientConnection)->[int,str]:
		if Client.AccountID == None:
			return 0
		else:
			return 1

	# 检查撤单信息
	def CheckCancelOrder(self,OrderID,Client):
		if self.CheckAccount(Client)==0:
			return 0,'账户ID异常'
		if Client.AccountID!=self.GetOrderByID(OrderID,["AccountID"])[0]:
			return 0,"账户ID不匹配"
		ret,msg=self.CheckOrderByID(OrderID)
		return ret,msg

# Exchange:拓展类
class Exchange(ExchangeBase):
	# 处理从柜台新推过来的订单数据
	def DealNewOrder(self,OrderID:uuid.UUID,Order:dict,Client:ClientConnection,MarkeSliNow=None)->[int,str]:
		ExchangeServerLogger.info("处理新报单:{},{}".format(OrderID,Order))
		# 检查新订单
		ret,msg=self.CheckNewOrder(OrderID,Order,Client)
		ExchangeServerLogger.debug("检查报单结果:{},{}".format(ret,msg))
		# 加入订单池
		if ret==1:ret,msg = self.AddOrder(OrderID, Order, Client)
		# 发送订单回报
		self.SendOrderReturn(OrderID,Client,ret,msg)
		# 检查不通过则退出
		if ret==0:return
		# 开始撮合
		ret,msg=self.MatchOrderByID(OrderID)
		return ret,msg

	# 撮合订单以及处理撮合结果
	def MatchOrderByID(self,OrderID:uuid.UUID)->[int,str]:
		ExchangeServerLogger.info("撮合订单:{}".format(OrderID))
		# 获取订单标的代码和柜台客户端
		Code,AccountID=self.GetOrderByID(OrderID,['Code','AccountID'])
		MktInfo = {'Price4Trd': self.MktSliNow.GetDataByCode(Code, 'Price'),
				   'Volume4Trd': self.MktSliNow.GetDataByCode(Code, 'Volume4Trd')}
		ret, msg, MatchInfo = self.MatchSimulation(OrderID, MktInfo)
		ExchangeServerLogger.debug("撮合结果:{},{},{}".format(ret, msg, MatchInfo))
		# 判断是否成交
		if MatchInfo['VolumeMatching'] == 0:
			return 1, '无成交'
		# 处理撮合结果
		# OrderPool更新
		ret,OrderState = self.DealMatchRetInOrderPool(OrderID, MatchInfo)
		ExchangeServerLogger.debug("OrderPool更新:{},{},{}".format(OrderID,ret, OrderState))
		# 市场行情切片也要处理撮合结果（扣除成交量等）
		self.MktSliNow.DealMatchRet(Code,MatchInfo)
		# 通知柜台处理成交回报
		ClientList=self.GetClientByAccountID(AccountID)
		[self.SendTransactionReturn(OrderID, Client, MatchInfo, OrderState, self.CreateMatchTime()) for Client in ClientList]
		return 1,''

	# 仿真撮合订单的函数
	# 需要用到订单数据，市场数据，柜台数据（费率等），其他撮合数据（如滑点，最大成交比例等）
	def MatchSimulation(self,OrderID:uuid.UUID,MktInfo:dict)->[int,str,dict]:
		ExchangeServerLogger.debug("仿真撮合:{},{}".format(OrderID,MktInfo))
		# 订单数据
		AccountID,OrderID,Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,Mkt,AddPar=self.GetOrderByID(OrderID)
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

	# 处理撮合结果
	def DealMatchRetInOrderPool(self,OrderID:uuid.UUID,MatchInfo:dict)->[int,str]:
		ExchangeServerLogger.debug("OrderPool处理撮合结果:{},{}".format(OrderID,MatchInfo))
		# 订单数据
		AccountID_Old,OrderID_Old,Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,Mkt_Old,AddPar_Old=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 开始处理
		# 计算新的订单记录的字段
		OrderID,Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,Mkt,AccountID,AddPar=OrderID_Old,Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,Mkt_Old,AccountID_Old,AddPar_Old
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
		ValueDict={
			"VolumeMatched": VolumeMatched,
			"State": State
		}
		self.UpdateOrderByID(OrderID,ValueDict)
		# 检查订单状态（如订单全部成交则需要删除等）
		ret,msg=self.CheckOrderByID(OrderID)
		ExchangeServerLogger.debug("检查订单结果:{},{}".format(ret, msg))
		return 1,State

	# 撤单函数
	def CancelOrder(self,OrderID:uuid.UUID,Client:ClientConnection)->[int,str]:
		ExchangeServerLogger.info("撤销订单:{}".format(OrderID))
		# 生成撤单时间
		CancelTime=self.CreateCancelTime()
		# 检查撤单是否有效
		ret,msg=self.CheckCancelOrder(OrderID,Client)
		ExchangeServerLogger.debug("检查撤单是否有效:{},{}".format(ret,msg))
		if ret==0:
			self.SendCancelOrderReturn(OrderID,Client,ret,msg,CancelTime)
			return 0,'撤单失败'
		# 删除订单
		ret,msg=self.DelOrderByID(OrderID)
		if ret==1:
			msg='撤单成功'
		# 发送撤单回报
		self.SendCancelOrderReturn(OrderID,Client,ret,msg,CancelTime)
		return ret,msg

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
	# E=ExchangeBase()
	# Order={
	# 		"Code": "000001.SZSE",
	# 		"Direction": 1,
	# 		"Price": 10.0,
	# 		"Volume": 100,
	# 		"AddPar":{'FeeFrozen': 10.0, 'CashBodyFrozenWhenOrdering': 1000.0, 'CashFrozen': 1010.0, 'FeeFrozenWhenOrdering': 10.0, 'CashFrozenWhenOrdering': 1010.0}
	# 	}
	# Client=ClientConnection(1,2,3,4)
	# Client.AccountID=uuid.uuid1()
	# E.AddOrder(uuid.uuid1(),Order,Client)
	# a=1