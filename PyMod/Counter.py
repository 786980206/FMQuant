# -*- coding: utf-8 -*-

import pandas as pd
import uuid
import datetime
import socket
import Common as cm
import time
import multiprocessing
import threading
import GeneralMod
from GeneralMod import ClientLogger
from DataServer import QOperation as Q
import DataDef as DataDef



Lock=threading.Lock()

# 账户基类，只有与交易所的简单交互
class AccountBase(object):
	# 初始化,账户持仓信息中暂时没考虑多空双向持仓
	def __init__(self,Usr:str, Pwd:str, AddPar:dict,Q:Q.Q=None,Type:str='Stock',AccPar:dict=DataDef.ACCOUNTPAR_DAFAULT,MktSliNow=None,WithGui:bool=False,ClientPutQueue=None,ClientGetQueue=None):
		ClientLogger.info("柜台账户初始化...")
		# 柜台信息
		self.AccountID = None
		self.Usr = Usr
		self.Pwd = Pwd
		self.AddPar = AddPar
		# 业务信息
		self.PositionTable ="Client_Position"
		self.OrderTable = "Client_Order"
		self.OrderRecTable ="Client_OrderRec"
		self.CashInfoTable ="Client_CashInfo"
		# self.CashInfo=self.SetCashInfoValue('',[0,0,0,0,pd.DataFrame(index=CASHFDETIAL_INDEX)])
		self.AccPar = AccPar  # 柜台账户参数数据，如账户手续费，保证金等数据
		self.MktSliNow = MktSliNow  # 当前行情切片，作为一个外部数据源供柜台模块引用
		# 连接信息
		self.ConnectionClient = None
		self.ConnectState = 0
		self.LogInState = 0
		# Gui信息
		self.WithGui=WithGui
		self.ClientPutQueue = ClientPutQueue
		self.ClientGetQueue = ClientGetQueue
		# 数据表操作信息
		self.Q=Q

	# 向交易所发送消息
	def SendMsgToExchange(self, Msg: dict) -> [int, str]:
		Msg = GeneralMod.MakeSendMsg(Msg)
		self.ConnectionClient.send(str(Msg).encode('utf-8'))
		ClientLogger.debug("成功发送消息:{}".format(Msg))
		return 1, "发送成功"

	# 连接和登录
	def ConnectAndLogin(self):
		# 绑定数据操作对象
		self.Q=DataDef.DataOperationObject
		# 开始连接服务器
		ret, msg = self.Connect(self.AddPar)
		ClientLogger.info("连接结果:{},{}".format(ret, msg))
		# 连接成功，开始登录和监听接收消息
		if ret == 1:
			try:
				# 开启监听服务器回报的线程
				MsgRecThread = threading.Thread(target=self.RecMsgFromExchange)
				# 子线程为守护线程
				MsgRecThread.daemon = True
				MsgRecThread.start()
				ClientLogger.debug("客户端消息监听线程启动")
				# 开始发送登录请求
				ret, msg = self.LogIn(self.Usr, self.Pwd)
				ClientLogger.debug("登录请求发送结果:{},{}".format(ret, msg))
				# 如果有Gui,Account线程开始等待Gui消息
				if self.WithGui:
					self.ListenFromGui()
			except Exception as e:
				print(e)
		elif ret == 0:
			self.SendMsgToGui({"MsgType": "LogInReturn", "ret": 0, "msg": "连接失败"})

	# 实盘账户初始化之后会连接柜台，获取交易参数等
	def Connect(self,AddPar:dict)->[int,str]:
		if AddPar["ExchangeServerHost"] !='':
			ConnectionClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			for TryTime in range(AddPar["MaxConnnectTryTime"]):
				try:
					ClientLogger.info("开始连接:{},{},第{}/{}次尝试...".format(AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"],TryTime+1,AddPar["MaxConnnectTryTime"]))
					ConnectionClient.connect((AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"]))
					self.ConnectState=1
					self.ConnectionClient=ConnectionClient
					return 1,"连接成功"
				except Exception as e:
					print(e)
					ClientLogger.warning("连接失败:{},{},等待{}s后重新连接...".format(AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"],AddPar["WaitTimeAfterTryConnect"]))
					time.sleep(AddPar["WaitTimeAfterTryConnect"])
			return 0, "连接失败"
		return 0,"连接地址无效"

	# 断连
	def DisConnect(self) -> None:
		self.ConnectionClient.close()
		self.ConnectionClient = None
		self.ConnectState = 0
		self.LogInState = 0
		self.AccountID=None
		ClientLogger.debug("断连成功")
		self.SendMsgToGui({"MsgType": "Disconnect"})

	# 重连
	def ReConnect(self) -> None:
		self.DisConnect()
		ClientLogger.info("开始重新连接...")
		self.SendMsgToGui({"MsgType": "Reconnect"})
		ret, msg = self.Connect(self.AddPar)
		if ret == 1:
			ClientLogger.info("重连成功")
			ret, msg = self.LogIn(self.Usr, self.Pwd)
			ClientLogger.debug("登录请求发送结果:{},{}".format(ret, msg))
			if ret == 1: self.RecMsgFromExchange()
		else:
			self.SendMsgToGui({"MsgType": "LogOut"})
			self.Exit()

	# 柜台连接服务器登录
	def LogIn(self, Usr: str, Pwd: str) -> [int, str]:
		Msg = {
			"MsgType": "LogIn",
			"Usr": Usr,
			"Pwd": Pwd
		}
		ClientLogger.info("发送登录请求:{}".format(Msg))
		ret, msg = self.SendMsgToExchange(Msg)
		if ret == 1:
			return 1, "登录请求发送成功"
		else:
			return 1, "登录请求发送失败"

	# 检查连接登录状态
	def CheckConnection(self) ->int:
		if self.ConnectState == 0:
			return 0
		elif self.LogInState == 0:
			return 0
		return 1

	# 退出
	def Exit(self) -> None:
		Msg = {
			"MsgType": "LogOut"
		}
		self.SendMsgToExchange(Msg)
		exit(0)

	# 接收消息Exchange的消息
	def RecMsgFromExchange(self):
		Lock = threading.Lock()
		Msg = ''
		while True:
			try:
				RecData = self.ConnectionClient.recv(DataDef.BUFFSIZE).decode('utf-8')
				ClientLogger.debug("读取缓冲区数据:{}".format(RecData))
			except:
				ClientLogger.warning("接收缓冲区数据失败!")
				if self.ConnectState == 1:
					self.ReConnect()
				else:
					exit(0)
			if RecData == '': self.Exit()
			Msglist, Msg = GeneralMod.AnalyzeMsg(Msg, RecData)
			for AimMsg in Msglist:
				try:
					with Lock:
						self.DealRecMsgFromExchange(AimMsg)
				except Exception as e:
					ClientLogger.error("处理消息出错:{},{}".format(AimMsg, e))

	# 处理从Exchange接收消息的函数
	def DealRecMsgFromExchange(self, Msg:dict):
		# 在子类中重写
		pass

	# 获取订单列表
	def GetOrderList(self)->[uuid.UUID]:
		if self.CheckConnection():
			pd_ret=self.Q.Query(self.OrderTable,["OrderID"],'AccountID="G"$("{}")'.format(self.AccountID))
			ret=list(pd_ret["OrderID"])
			return ret
		else:
			return []

	# 获取所有的订单列表,含有成交和撤销的
	def GetAllOrderList(self)->[uuid.UUID]:
		if self.CheckConnection():
			pd_ret=self.Q.Query(self.OrderRecTable,["OrderID"],'AccountID="G"$("{}")'.format(self.AccountID))
			ret=list(pd_ret["OrderID"])
			return ret
		else:
			return []

	# 获取订单数据
	def GetOrderByID(self,OrderID:uuid.UUID,Fields:list=DataDef.ORDER_INDEX)->list:
		if self.CheckConnection():
			# 从OrderRec中获取,能保证一定获取到
			if OrderID in self.GetAllOrderList():
				pd_ret = self.Q.Query(self.OrderRecTable, Fields,'AccountID="G"$("{}"),OrderID="G"$("{}")'.format(self.AccountID, OrderID))
				ret = list(pd_ret.iloc[0])
				return ret
			else:
				return [None]*len(Fields)
		else:
			return [None] * len(Fields)

	# 记录新订单，将新订单加入订单记录中并生成订单id
	def AddOrder(self, Order: dict) -> [int, str, uuid.UUID]:
		if self.CheckConnection():
			Code = Order['Code']
			Direction = Order['Direction']
			Price = Order['Price']
			Volume = Order['Volume']
			AddPar = Order['AddPar']
			# 生成订单编号
			OrderID = self.CreateOrderID()
			# 记录订单
			ClientLogger.info("记录订单:{},{}".format(OrderID, Order))
			ValueDict = {
				"AccountID": [self.AccountID],
				"OrderID": [OrderID],
				"Code": [Code],
				"Direction": [Direction],
				"Price": [Price],
				"Volume": [Volume],
				"VolumeMatched": [0],
				"State": ["SendToMatch"],
				"AvgMatchingPrice": [0],
				"OrderTime": [self.CreateOrderTime()],
				"Mkt": [cm.GetExchangeByCode(Code)],
				"AddPar": [AddPar]
			}
			# 记录在Order和OrderRec中
			self.Q.Insert(self.OrderTable, ValueDict)
			self.Q.Insert(self.OrderRecTable, ValueDict)
			ClientLogger.info("记录订单成功:{}".format(OrderID))
			self.RefreshOrderMsgForGui()
			return 1, "增加订单记录成功", OrderID
		else:
			return 0, "登录状态异常", ""

	# 删除订单
	def DelOrderByID(self, OrderID: uuid.UUID) -> [int, str]:
		if self.CheckConnection():
			if OrderID in self.GetOrderList():
				# 只删除Order的，不删除OrderRec的
				self.Q.Del(self.OrderTable, 'AccountID="G"$("{}"),OrderID="G"$("{}")'.format(self.AccountID, OrderID))
				ClientLogger.info("清除订单成功:{}".format(OrderID))
				self.RefreshOrderMsgForGui()
				return 1, "删除订单记录成功"
			else:
				return 0, "订单不存在"
		else:
			return 0, "登录状态异常"

	# 删除OrderRec
	def DelOrderRecByID(self, OrderID: uuid.UUID) -> [int, str]:
		if self.CheckConnection():
			if OrderID in self.GetAllOrderList():
				self.Q.Del(self.OrderRecTable, 'AccountID="G"$("{}"),OrderID="G"$("{}")'.format(self.AccountID, OrderID))
				ClientLogger.info("清除订单成功:{}".format(OrderID))
				self.RefreshOrderMsgForGui()
				return 1, "删除订单记录成功"
			else:
				return 0, "订单不存在"
		else:
			return 0, "登录状态异常"

	# 更新订单状态的函数
	def UpdateOrderByID(self, OrderID: uuid.UUID, ValueDict: dict) -> [int, str]:
		if self.CheckConnection():
			if OrderID in self.GetOrderList():
				# 更新Order与OrderRec
				self.Q.Update(self.OrderTable, ValueDict,
							  'AccountID="G"$("{}"),OrderID="G"$("{}")'.format(self.AccountID, OrderID))
				self.Q.Update(self.OrderRecTable, ValueDict,
							  'AccountID="G"$("{}"),OrderID="G"$("{}")'.format(self.AccountID, OrderID))
				ClientLogger.debug("更新订单状态:{},{}".format(OrderID,ValueDict))
				self.RefreshOrderMsgForGui()
			else:
				return 0, "订单不存在"
		else:
			return 0, "登录状态异常"

	# 获取持仓列表
	def GetPositionList(self) -> [str]:
		if self.CheckConnection():
			pd_ret = self.Q.Query(self.PositionTable, ["Code"], 'AccountID="G"$("{}")'.format(self.AccountID))
			ret = list(pd_ret["Code"])
			return ret
		else:
			return []

	# 获取持仓信息
	def GetPositionByCode(self, Code: str, Fields: list = DataDef.POSITION_INDEX) -> list:
		if self.CheckConnection():
			if Code in self.GetPositionList():
				pd_ret = self.Q.Query(self.PositionTable, Fields,
									  'AccountID="G"$("{}"),Code=`{}'.format(self.AccountID, Code))
				ret = list(pd_ret.iloc[0])
				return ret
			else:
				return [None] * len(Fields)
		else:
			return [None] * len(Fields)

	# 记录新持仓
	def AddPosition(self, Code: str) -> [int, str]:
		if self.CheckConnection():
			if Code not in self.GetPositionList():
				ValueDict = {
					"AccountID": [self.AccountID],
					"Code": [Code],
					"Vol": [0],
					"VolA": [0],
					"VolF": [0],
					"StockActualVol": [0],
					"AvgCost": [0],
					"PriceNow": [0],
					"MktValue": [0],
					"FloatingProfit": [0],
					"ProfitRatio": [0],
					"Currency": ["CNY"],
					"Mkt": [cm.GetExchangeByCode(Code)],
					"AddPar": [{}],
				}
				self.Q.Insert(self.PositionTable, ValueDict)
				ClientLogger.debug("新增持仓:{}".format(self.GetPositionByCode(Code)))
				self.RefreshPositionMsgForGui()
				return 1, "增加持仓记录成功"
		else:
			return 0, "登录状态异常"

	# 更新持仓状态
	def UpdatePositionByCode(self, Code: str, ValueDict: dict):
		if self.CheckConnection():
			if Code in self.GetPositionList():
				self.Q.Update(self.PositionTable, ValueDict,
							  'AccountID="G"$("{}"),Code=`{}'.format(self.AccountID, Code))
				ClientLogger.debug("更新持仓状态:{},{}".format(Code,ValueDict))
				self.RefreshPositionMsgForGui()
				return 1, "更新持仓成功"
			else:
				return 0, "持仓不存在"
		else:
			return 0, "登录状态异常"

	# 删除持仓
	def DelPositionByCode(self, Code: str) -> [int, str]:
		if self.CheckConnection():
			if Code in self.GetPositionList():
				self.Q.Del(self.PositionTable, 'AccountID="G"$("{}"),Code=`{}'.format(self.AccountID, Code))
				ClientLogger.info("清除持仓成功:{}".format(Code))
				self.RefreshPositionMsgForGui()
				return 1, "删除持仓记录成功"
			else:
				return 0, "持仓不存在"
		else:
			return 0, "登录状态异常"

	# 查询资金状态的函数
	def GetCashInfo(self, Fields: list = DataDef.CASHINFO_INDEX) -> list:
		if self.CheckConnection():
			pd_ret = self.Q.Query(self.CashInfoTable, Fields, 'AccountID="G"$("{}")'.format(self.AccountID))
			ret = list(pd_ret.iloc[0])
			return ret
		else:
			return [None ] *len(Fields)

	# 更新资金状态的函数
	def UpdateCashInfo(self ,ValueDict :dict )->[int ,str]:
		if self.CheckConnection():
			self.Q.Update(self.CashInfoTable ,ValueDict ,'AccountID="G"$("{}")'.format(self.AccountID))
			self.RefreshCashInfoMsgForGui()
			return 1 ,"更新资金状态成功"
		else:
			return 0 ,"登录状态异常"


	# 生成订单ID
	def CreateOrderID(self)->uuid.UUID:
		return uuid.uuid1()

	# 生成订单下单时间
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 发送消息给Gui
	def SendMsgToGui(self,Msg:dict)->None:
		if self.WithGui:
			self.ClientPutQueue.put(Msg)
			ClientLogger.debug("向Gui发送消息:{}".format(Msg))

	# 向Gui发送验单回报,还未发送到Exchange，只是在Exchange验了
	def SendOrderCheckRet(self, ret:int, msg:str):
		if self.WithGui:
			MsgRet = {"MsgType": "RetCheckOrder", "ret": ret, "msg": msg}
			self.SendMsgToGui(MsgRet)

	# 更新GUI的信息
	def RefreshOrderMsgForGui(self):
		if self.WithGui:
			OrderList = self.GetOrderList()
			ret = [self.GetOrderByID(x) for x in OrderList]
			MsgRet = {"MsgType": "RetOrderList", "Order": ret}
			self.SendMsgToGui(MsgRet)

	def RefreshPositionMsgForGui(self):
		if self.WithGui:
			PositionList = self.GetPositionList()
			ret = [self.GetPositionByCode(x) for x in PositionList]
			MsgRet = {"MsgType": "RetPositionList", "Position": ret}
			self.SendMsgToGui(MsgRet)

	def RefreshCashInfoMsgForGui(self):
		if self.WithGui:
			ret = self.GetCashInfo()
			MsgRet = {"MsgType": "RetCashInfo", "CashInfo": ret}
			self.SendMsgToGui(MsgRet)

	# 监听接收界面消息
	def ListenFromGui(self):
		while 1:
			Msg=self.ClientGetQueue.get()
			self.DealRecMsgFromGui(Msg)

	# 处理界面传递的消息
	def DealRecMsgFromGui(self,Msg:dict):
		# 在子类中重写
		pass


class Account(AccountBase):
	# 处理从Exchange接收消息的函数=============================================================================================================================
	def DealRecMsgFromExchange(self, Msg:dict):
		ClientLogger.debug("处理消息:{}".format(Msg))
		# 发送到Gui
		self.SendMsgToGui(Msg)
		# 测试打印字符串
		if Msg['MsgType'] == "Print":
			print('处理接收消息的线程打印：{}'.format(Msg))
		# 退出
		if Msg['MsgType'] == "Exit":
			self.Exit()
		# 登录成功回报
		if Msg['MsgType'] == "LogInReturn":
			self.LogInState = 1
			self.AccountID=Msg["AccountID"]
			ClientLogger.info("登录成功:{}".format(Msg))
		# 下单回报
		if Msg['MsgType'] == "OrderReturn":
			self.DealOrderPlaceRet(uuid.UUID(Msg['OrderID']), Msg["ret"], Msg["msg"], Msg["OrderTime"])
		# 撤单回报
		if Msg['MsgType'] == "CancelOrderReturn":
			self.DealOrderCancelRet(uuid.UUID(Msg['OrderID']), Msg["ret"], Msg["msg"], Msg["CancelTime"])
		# 成交回报
		if Msg['MsgType'] == "TransactionReturn":
			self.DealOrderMatchRet(uuid.UUID(Msg['OrderID']), Msg["MatchInfo"], Msg["MatchTime"])


	# 处理订单回报
	def DealOrderPlaceRet(self,OrderID:uuid.UUID,ret:int,msg:str,OrderTime:str):
		ClientLogger.info("处理订单回报:{},{},{},{}".format(OrderID,ret,msg,OrderTime))
		if ret==1:
			ValueDict={
				"State":"WaitToMatch",
				"OrderTime":OrderTime
			}
			self.UpdateOrderByID(OrderID,ValueDict)

	# 处理撤单回报
	def DealOrderCancelRet(self,OrderID:uuid.UUID,ret:int,msg:str,CancelTime:str):
		ClientLogger.info("处理撤单回报:{},{},{},{}".format(OrderID,ret,msg,CancelTime))
		if ret==1:
			AddPar=self.GetOrderByID(OrderID,["AddPar"])[0]
			AddPar["CancelTime"]=CancelTime
			ValueDict={
				"State":"Canceled",
				"AddPar":AddPar
			}
			self.UpdateOrderByID(OrderID,ValueDict)
			# 检查订单状态，将订单冻结的资金等归还和清除订单
			self.CheckOrderByID(OrderID)

	# 检查订单状态（如订单全部成交则需要删除等）
	def CheckOrderByID(self,OrderID:uuid.UUID)->[int,str]:
		ClientLogger.debug("检查订单状态:{}".format(OrderID))
		# 订单数据
		Volume,VolumeMatched,State,AddPar=self.GetOrderByID(OrderID,['Volume','VolumeMatched','State','AddPar'])
		# 判断是否全部成交
		if (Volume==VolumeMatched and State=='AllMatched') or State=="Canceled":
			# 订单解冻
			self.UnFrozenOrder(OrderID)
			# 清除订单
			self.DelOrderByID(OrderID)
		elif AddPar["FeeFrozen"]!=0 and (State=="WaitToMatch" or State=="SendToMatch"):
			ClientLogger.error("订单状态异常:{},{}".format(OrderID,[Volume,VolumeMatched,State,AddPar]))
			# 设置异常状态
			ValueDict={
				"State":"Error"
			}
			self.UpdateOrderByID(OrderID,ValueDict)
			# 清除订单
			self.DelOrderByID(OrderID)
		return 1,''

	# 将订单资金等解冻
	def UnFrozenOrder(self,OrderID:uuid.UUID)->[int,str]:
		Code, Volume, VolumeMatched,Direction,AddPar = self.GetOrderByID(OrderID, ['Code', 'Volume','VolumeMatched', 'Direction','AddPar'])
		ClientLogger.debug("资金解冻:{},{}".format(OrderID, [Code, Volume, VolumeMatched,Direction,AddPar]))
		# 买入解冻资金
		if Direction==1:
			CashFrozen,FeeFrozen=AddPar["CashFrozen"],AddPar["FeeFrozen"]
			ValueDict={
				'CashA': self.GetCashInfo(['CashA'])[0] + CashFrozen,
				'CashF': self.GetCashInfo(['CashF'])[0] - CashFrozen,
			}
			self.UpdateCashInfo(ValueDict)
			# 订单更新
			AddPar["CashFrozen"], AddPar["FeeFrozen"] = 0, 0
			ValueDict={
				"AddPar":AddPar
			}
			self.UpdateOrderByID(OrderID,ValueDict)
		elif Direction==0:
			# 持仓解冻
			VolumeFrozen,FeeFrozen=AddPar["VolumeFrozen"],AddPar["FeeFrozen"]
			ValueDict={
				"VolA":self.GetPositionByCode(Code,["VolA"])[0]+VolumeFrozen,
				"VolF": self.GetPositionByCode(Code, ["VolF"])[0] - VolumeFrozen
			}
			self.UpdatePositionByCode(Code,ValueDict)
			# 资金解冻
			AddPar["CashFrozen"], AddPar["FeeFrozen"] = 0, 0
			ValueDict={
				'CashA': self.GetCashInfo(['CashA'])[0] + FeeFrozen,
				'CashF': self.GetCashInfo(['CashF'])[0] - FeeFrozen
			}
			self.UpdateCashInfo(ValueDict)
			# 订单更新
			AddPar["CashFrozen"], AddPar["FeeFrozen"] = 0, 0
			ValueDict = {
				"AddPar": AddPar
			}
			self.UpdateOrderByID(OrderID, ValueDict)
		return 1,'资金持仓解冻成功！'

	# 处理订单成交回报
	def DealOrderMatchRet(self,OrderID:uuid.UUID,MatchInfo:dict,MatchTime:str):
		ClientLogger.info("处理成交回报:{},{},{}".format(OrderID,MatchInfo,MatchTime))
		# 计算资金费用等
		CalcRet=self.CalcOrderMatchFee(OrderID,MatchInfo)
		# 更新订单列表
		ret,msg=self.DealMatchRetInOrderList(OrderID,MatchInfo,CalcRet)
		# 更新持仓列表
		ret,msg=self.DealMatchRetInPositionList(OrderID,MatchInfo,CalcRet)
		# 更新资金列表
		ret,msg=self.DealMatchRetInCashInfo(OrderID,MatchInfo,CalcRet)
		return 1,''

	# 根据成交回报处理OrderList
	def DealMatchRetInOrderList(self, OrderID:uuid.UUID, MatchInfo:dict, CalcRet:dict)->[int,str]:
		ClientLogger.debug("更新订单列表:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		AccountID_Old,OrderID_Old,Code_Old, Direction_Old, Price_Old, Volume_Old, VolumeMatched_Old, State_Old, AvgMatchingPrice_Old, OrderTime_Old, Mkt_Old, AddPar_Old = self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching = MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Old==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody, Fee, CashCalc = CalcRet["CashBody"], CalcRet["Fee"], CalcRet["CashCalc"]
		# 开始处理
		# 计算新的订单记录的字段
		AccountID,OrderID,Code, Direction, Price, Volume, VolumeMatched, State, AvgMatchingPrice, OrderTime, Mkt, AddPar = AccountID_Old,OrderID_Old,Code_Old, Direction_Old, Price_Old, Volume_Old, VolumeMatched_Old, State_Old, AvgMatchingPrice_Old, OrderTime_Old, Mkt_Old, AddPar_Old
		# 已成交量
		VolumeMatched = VolumeMatched_Old + VolumeMatching
		# 状态
		# 如果已成=订单量
		if VolumeMatched == Volume_Old:
			State = 'AllMatched'
		elif VolumeMatched < Volume_Old and VolumeMatched != 0:
			State = 'PartMatched'
		else:
			State = 'WaitToMatch'
		# 成交均价=（此前成交总价+本次成交金额（计算了费用的））/总已成量
		AvgMatchingPrice = (VolumeMatched_Old * AvgMatchingPrice_Old + CashCalc) / VolumeMatched
		# 冻结资金计算
		if Direction == 1:
			AddPar["CashFrozen"] = AddPar["CashFrozen"] - CashCalc
			AddPar["FeeFrozen"] = AddPar["FeeFrozen"] - Fee
			AddPar["FeeConfirm"] = AddPar["FeeConfirm"] + Fee if "FeeConfirm" in AddPar else Fee
		elif Direction == 0:
			AddPar["VolumeFrozen"] = AddPar["VolumeFrozen"] - VolumeMatched
			AddPar["FeeFrozen"] = AddPar["FeeFrozen"] - Fee
			AddPar["FeeConfirm"] = AddPar["FeeConfirm"] + Fee if "FeeConfirm" in AddPar else Fee
		# 回写数据到Order及OrderRec
		ValueDict={
			"AccountID": AccountID,
			"OrderID": OrderID,
			"Code": Code,
			"Direction": Direction,
			"Price": Price,
			"Volume": Volume,
			"VolumeMatched": VolumeMatched,
			"State": State,
			"AvgMatchingPrice": AvgMatchingPrice,
			"OrderTime": OrderTime,
			"Mkt": Mkt,
			"AddPar": AddPar
		}
		self.UpdateOrderByID(OrderID,ValueDict)
		# 检查订单状态（如订单全部成交则需要取消等）
		ret, msg = self.CheckOrderByID(OrderID)
		return 1, ''

	# 根据成交回报处理PositionList
	def DealMatchRetInPositionList(self, OrderID:uuid.UUID, MatchInfo:dict, CalcRet:dict)->[int,str]:
		ClientLogger.debug("更新持仓列表:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		AccountID_Order,OrderID_Order,Code_Order, Direction_Order, Price_Order, Volume_Order, VolumeMatched_Order, State_Order, AvgMatchingPrice_Order, OrderTime_Order, Mkt_Order, AddPar_Order = self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching = MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody, Fee, CashCalc = CalcRet["CashBody"], CalcRet["Fee"], CalcRet["CashCalc"]
		# 判断是否已有持仓
		if Code_Order not in self.GetPositionList():
			self.AddPosition(Code_Order)
		AccountID_Position,Code_Position, Vol_Position, VolA_Position, VolF_Position, StockActualVol_Position, AvgCost_Position, PriceNow_Position, MktValue_Position, FloatingProfit_Position, ProfitRatio_Position, Currency_Position, Mkt_Position, AddPar_Position = self.GetPositionByCode(Code_Order)
		# 初始化持仓字段
		AccountID,Code, Vol, VolA, VolF, StockActualVol, AvgCost, PriceNow, MktValue, FloatingProfit, ProfitRatio, Currency, Mkt, AddPar = AccountID_Position,Code_Position, Vol_Position, VolA_Position, VolF_Position, StockActualVol_Position, AvgCost_Position, PriceNow_Position, MktValue_Position, FloatingProfit_Position, ProfitRatio_Position, Currency_Position, Mkt_Position, AddPar_Position
		# 计算持仓字段
		# 主要分多空
		if Direction_Order == 1:
			Vol = Vol_Position + VolumeMatching
			VolA = VolA_Position  # 股票T+1，可用量不变
			AddPar["FrozenToday"] = AddPar_Position[
										"FrozenToday"] + VolumeMatching if "FrozenToday" in AddPar_Position else VolumeMatching
			VolF = VolF_Position + VolumeMatching
			StockActualVol = StockActualVol_Position
			AvgCost = (AvgCost_Position * Vol_Position + CashCalc) / Vol
		elif Direction_Order == 0:
			Vol = Vol_Position - VolumeMatching
			VolA = VolA
			VolF = VolF_Position - VolumeMatching
			StockActualVol = StockActualVol_Position
			# 卖出平均成本=0 if 持仓=0 else （旧的平均成本*旧的持仓量-卖出收回资金）/新持仓量
			AvgCost = 0 if Vol == 0 else (AvgCost_Position * Vol_Position - CashCalc) / Vol
		# 回写数据到持仓数据中
		# 因为其他的字段都和实时行情有关，回写完毕后重新调用一个函数即可
		ValueDict={
			"AccountID": AccountID,
			"Code": Code,
			"Vol": Vol,
			"VolA": VolA,
			"VolF": VolF,
			"StockActualVol":StockActualVol,
			"AvgCost": AvgCost,
			"PriceNow": PriceNow,
			"MktValue":MktValue,
			"FloatingProfit": FloatingProfit,
			"ProfitRatio": ProfitRatio,
			"Currency": Currency,
			"Mkt": Mkt,
			"AddPar": AddPar
		}
		self.UpdatePositionByCode(Code,ValueDict)
		# 重新计算实时持仓盈亏
		ret, msg = self.CalcPositionRealTimeValueByCode(Code)
		# 检查持仓信息（如无效持仓清除等）
		ret, msg = self.CheckPositionByCode(Code)
		return 1, ''

	# 更新资金信息CashInfo
	def DealMatchRetInCashInfo(self, OrderID:uuid.UUID, MatchInfo:dict, CalcRet:dict)->[int,str]:
		ClientLogger.debug("更新资金信息:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		AccountID_Order,OrderID_Order,Code_Order, Direction_Order, Price_Order, Volume_Order, VolumeMatched_Order, State_Order, AvgMatchingPrice_Order, OrderTime_Order, Mkt_Order, AddPar_Order = self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		# VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody, Fee, CashCalc = CalcRet["CashBody"], CalcRet["Fee"], CalcRet["CashCalc"]
		# 资金数据
		Cash_Old,InitCash_Old,CashA_Old,CashF_Old = self.GetCashInfo(['Cash','InitCash','CashA','CashF'])
		# 开始计算
		# 买入计算
		if Direction_Order == 1:
			Cash = Cash_Old - CashCalc
			InitCash = InitCash_Old
			CashA = CashA_Old
			CashF = CashF_Old - CashCalc
		elif Direction_Order == 0:
			# CashCalc=CashBody-Fee
			Cash = Cash_Old + CashCalc
			InitCash = InitCash_Old
			CashA = CashA_Old + CashCalc
			# 费用确认：卖出的话冻结资金要减去冻结的费用,可用资金要加上费用（可用资金在下单的时候就扣除了，成交时不用扣除）
			CashF = CashF_Old - Fee
			CashA = CashA + Fee
		# 回写数据
		ValueDict={
			"Cash":Cash,
			"InitCash":InitCash,
			"CashA":CashA,
			"CashF":CashF
		}
		self.UpdateCashInfo(ValueDict)
		ClientLogger.debug("资金信息:{}".format(self.GetCashInfo(['Cash', 'InitCash', 'CashA', 'CashF'])))
		return 1, ''

	# 计算实时持仓价值
	def CalcPositionRealTimeValueByCode(self, Code:str)->[int,str]:
		ClientLogger.debug("计算实时持仓价值:{}".format(Code))
		if Code not in self.GetPositionList(): return 0, '无效Code！'
		# 市场数据
		Price = self.MktSliNow.GetDataByCode(Code, 'Price')
		# 更新数据
		Vol,AvgCost=self.GetPositionByCode(Code, ['Vol',"AvgCost"])
		ValueDict={
			"PriceNow":Price,
			"MktValue":Price * Vol,
			"FloatingProfit":(Price - AvgCost) * Vol,
			"ProfitRatio":(Price - AvgCost) / AvgCost if AvgCost != 0 else 0
		}

		self.UpdatePositionByCode(Code,ValueDict)
		ClientLogger.debug("持仓数据:{}".format(self.GetPositionByCode(Code)))
		return 1, ''


	# 检查持仓数据（如无效持仓需要清理等）
	def CheckPositionByCode(self, Code):
		ClientLogger.debug("检查持仓信息:{}".format(Code))
		# 持仓数据
		Vol = self.GetPositionByCode(Code, ['Vol'])[0]
		# 判断是否全部成交
		if Vol == 0:
			# 清除持仓
			self.DelPositionByCode(Code)
		elif Vol == None:
			# 本来就没持仓了
			pass
		return 1, ''

	# 处理界面传递的消息=======================================================================================================================================
	def DealRecMsgFromGui(self,Msg:dict):
		ClientLogger.debug("接收GUI消息:{}".format(Msg))
		if Msg["MsgType"]=="GetAccountInfo":
			self.RefreshOrderMsgForGui()
			self.RefreshPositionMsgForGui()
			self.RefreshCashInfoMsgForGui()
		if Msg["MsgType"] == "GetOrderInfo":
			self.RefreshOrderMsgForGui()
		if Msg["MsgType"] == "GetPositionInfo":
			self.RefreshPositionMsgForGui()
		if Msg["MsgType"] == "GetCashInfo":
			self.RefreshCashInfoMsgForGui()
		if Msg["MsgType"] == "PlaceOrder":
			self.PlaceOrder(*Msg["Order"])
		if Msg["MsgType"] == "CancelOrder":
			self.CancelOrder(Msg["OrderID"])
		if Msg["MsgType"] == "LogOut":
			self.Exit()

	# 账户下单
	def PlaceOrder(self,Code:str,Direction:int,Price:float,Volume:int,AddPar:dict=None)->[int,str,uuid.UUID]:
		# 检查连接登录状态等
		ret=self.CheckConnection()
		if ret==0:return ret,"登录状态异常"
		# 开始下单
		ClientLogger.info("账户下单:{}".format([Code,Direction,Price,Volume,AddPar]))
		Order={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'AddPar':AddPar}
		# 验单
		MktInfo={'Price_LimitUp':self.MktSliNow.GetDataByCode(Code,'Price_LimitUp'),'Price_LimitDown':self.MktSliNow.GetDataByCode(Code,'Price_LimitDown')}
		ret,msg=self.CheckNewOrder(Order,MktInfo)
		ClientLogger.info("验单结果:{},{}".format(ret,msg))
		self.SendOrderCheckRet(ret,msg)
		if ret==0:
			return ret,msg,''
		else:
			# 记录订单
			ret,msg,OrderID=self.AddOrder(Order)
			# 资金冻结
			ret,msg=self.FrozenNewOrder(OrderID)
			# 发送到交易所撮合
			ret,msg=self.SendNewOrderToMatch(OrderID)
		return ret,msg,OrderID

	# 订单校验
	# 验单进行资金冻结等
	# 需求参数：账户信息，订单信息(其中账户信息，参照CTP，可以自己进行订单验证)，验单需要的其他信息，如涨跌停价格
	# 主要内容：1.判断价格是否正确（涨跌停以内）;2.判断可用资金和可用量是否充足。
	def CheckNewOrder(self,Order:dict,MktInfo:dict)->[int,str]:
		ClientLogger.debug("柜台验单:{},{}".format(Order,MktInfo))
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# 判断代码是否有效
		ret=cm.CheckCode(Code)
		if ret==0:return ret,"代码无效"
		# 判断是否在涨跌停价格以内
		if Price!=0 and (Price>MktInfo['Price_LimitUp'] or Price<MktInfo['Price_LimitDown']):
			ret=0
			msg='价格不在有效的区间范围内'
			return ret,msg
		# 判断订单数量是否被100整除(卖出数量可以为小于100的散股)
		if Direction==1 and (Volume % 100!=0 or Volume<=0) :
			ret=0
			msg='输入订单数量无效！'
			return ret,msg
		elif Direction==0:
			PositionVolume=(self.GetPositionByCode(Code,['Vol'])[0] if self.GetPositionByCode(Code,['Vol'])[0]!=None else 0)
			if PositionVolume<100 and PositionVolume>0:
				# 总持仓小于100且大于0的卖出单，可以为非100的整数倍
				pass
			elif (Volume % 100!=0 or Volume<=0):
				ret = 0
				msg = '输入订单数量无效！'
				return ret, msg
		# 其他判断
		if Direction==1:
			CommissionRate=self.AccPar['CommissionRate']
			# 判断是不是市价下单,是的话，价格按涨停价格下单冻结资金
			if Price==0:
				Price2Frozen=MktInfo['Price_LimitUp']
			else:
				Price2Frozen=Price
			if Volume*Price2Frozen*(1+CommissionRate)>self.GetCashInfo(['CashA'])[0]:
				ret=0
				msg='可用资金不足，订单无效'
				return ret,msg
		elif Direction==0:
			if Volume>(self.GetPositionByCode(Code,['VolA'])[0] if self.GetPositionByCode(Code,['VolA'])[0]!=None else 0):
				ret=0
				msg='可用持仓不足，订单无效'
				return ret,msg
		return 1,'订单有效'

	# 冻结资金持仓等
	# 验单通过的订单进行冻结资金的操作
	# 这里没有数据锁，可能出现验单通过实际冻结的时候却不足的问题吗？
	def FrozenNewOrder(self,OrderID:uuid.UUID)->[int,str]:
		Code,Volume,Direction=self.GetOrderByID(OrderID,['Code','Volume','Direction'])
		ClientLogger.debug("冻结资金:{}".format(OrderID))
		# 计算费用
		FeeCalc = self.CalcOrderPlaceFee(OrderID)
		CashBody, Fee, CashCalc = FeeCalc['CashBody'], FeeCalc['Fee'], FeeCalc['CashCalc']
		# 买入冻结资金
		if Direction==1:
			ValueDict={
				"CashA":self.GetCashInfo(['CashA'])[0] - CashCalc,
				"CashF":self.GetCashInfo(['CashF'])[0] + CashCalc
			}
			self.UpdateCashInfo(ValueDict)
			# 在订单中进行记录
			AddPar=self.GetOrderByID(OrderID,["AddPar"])[0]
			AddPar["CashFrozen"]=CashCalc
			AddPar["FeeFrozen"]=Fee
			AddPar["CashFrozenWhenOrdering"] = CashCalc
			AddPar["CashBodyFrozenWhenOrdering"] = CashBody
			AddPar["FeeFrozenWhenOrdering"] = Fee
			ValueDict={
				"AddPar":AddPar
			}
			self.UpdateOrderByID(OrderID,ValueDict)
		elif Direction==0:
			# 卖出冻结手续费
			ValueDict = {
				"CashA": self.GetCashInfo(['CashA'])[0] - Fee,
				"CashF": self.GetCashInfo(['CashF'])[0] + Fee
			}
			self.UpdateCashInfo(ValueDict)
			# 冻结持仓
			ValueDict = {
				"VolA": self.GetPositionByCode(Code, ["VolA"])[0] - Volume,
				"VolF": self.GetPositionByCode(Code, ["VolF"])[0] + Volume
			}
			self.UpdatePositionByCode(Code, ValueDict)
			# 在订单中进行记录
			AddPar = self.GetOrderByID(OrderID, ["AddPar"])[0]
			AddPar["VolumeFrozen"] = Volume
			AddPar["FeeFrozen"] = Fee
			AddPar["VolumeFrozenWhenOrdering"] = Volume
			AddPar["FeeFrozenWhenOrdering"] = Fee
			ValueDict = {
				"AddPar": AddPar,
			}
			self.UpdateOrderByID(OrderID, ValueDict)

		return 1,'冻结资金持仓成功！'

	# 发送新订单到“虚拟交易所”进行撮合
	def SendNewOrderToMatch(self,OrderID:uuid.UUID)->[int,str]:
		Code,Direction,Price,Volume,AddPar=self.GetOrderByID(OrderID,['Code','Direction','Price','Volume','AddPar'])
		Msg={
			"MsgType": "PlaceOrder",
			"Order": {"Code": Code, "Direction": Direction, "Price": Price, "Volume": Volume, "AddPar": AddPar},
			"OrderID": str(OrderID)
		}
		ClientLogger.info("发送下单请求:{}".format(Msg))
		self.SendMsgToExchange(Msg)
		return 1,"发送成功"

	# 撤单函数
	def CancelOrder(self,OrderID:uuid.UUID)->None:
		ClientLogger.info("撤销订单:{}".format(OrderID))
		# 验单
		if self.CheckCancelOrder(OrderID):
			self.SendOrderToCancel(OrderID)

	# 检验准备撤的单是否有效
	def CheckCancelOrder(self,OrderID:uuid.UUID)->bool:
		if OrderID in self.GetOrderList():
			return 1
		return 0

	# 发送撤单信息
	def SendOrderToCancel(self,OrderID:uuid.UUID)->None:
		ClientLogger.info("发送撤单信息:{}".format(OrderID))
		Msg={
			"MsgType":"CancelOrder",
			"OrderID":str(OrderID)
		}
		ret,msg=self.SendMsgToExchange(Msg)

	# 计算下单手续费等
	def CalcOrderPlaceFee(self,OrderID:uuid.UUID)->dict:
		ClientLogger.debug("计算下单手续费:{}".format(OrderID))
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,Mkt_Order=self.GetOrderByID(OrderID,["Code","Direction","Price","Volume","Mkt"])
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
		# 市场数据
		Price_LimitUp=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitUp')
		Price_LimitDown=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitDown')
		# 开始计算
		# 根据计算时机不同而不同，可能在下单冻结计算或在成交清算计算
		if Price_Order==0 and Direction_Order==1:
			# 计算市价买入冻结金额
			Price2Calc=Price_LimitUp
			Volume2Calc=Volume_Order
		elif Price_Order!=0 and Direction_Order==1:
			# 计算限价买入冻结金额
			Price2Calc=Price_Order
			Volume2Calc=Volume_Order
		else:
			# 卖出计算金额,虽然不冻结资金，但是印花税费需要按最大的计算冻结
			Price2Calc=Price_LimitUp
			Volume2Calc=Volume_Order
		# 费用主体,成交金额
		CashBody=Price2Calc*Volume2Calc
		# 佣金
		CommissionFee=5 if CashBody*CommissionRate<5 else CashBody*CommissionRate
		# 印花税费=卖出成交额*0.001
		StampFee=CashBody*0.001 if Direction_Order==0 else 0
		# 过户费，仅上海股票
		if Mkt_Order=='SHSE':
			TransferFee=1 if Price2Calc/1000<1 else Volume2Calc/1000
		else:
			TransferFee=0
		# 所有费用
		Fee=CommissionFee+StampFee+TransferFee
		# 加减过Fee的CashBody
		CashCalc=CashBody+Fee if Direction_Order==1 else CashBody-Fee
		# 返回结果
		return {'CashBody':CashBody,'Fee':Fee,'CashCalc':CashCalc,'CommissionFee':CommissionFee,'StampFee':StampFee,'TransferFee':TransferFee}

	# 计算成交手续费等
	def CalcOrderMatchFee(self,OrderID:uuid.UUID,MatchInfo:dict)->dict:
		ClientLogger.debug("计算成交手续费:{},{}".format(OrderID,MatchInfo))
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,Mkt_Order=self.GetOrderByID(OrderID,["Code","Direction","Price","Volume","Mkt"])
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
		# 市场数据
		Price_LimitUp=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitUp')
		Price_LimitDown=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitDown')
		# 开始计算
		# 根据成交回报计算交易金额
		Price2Calc=MatchInfo['PriceMatching']
		Volume2Calc=MatchInfo['VolumeMatching']
		# 费用主体
		CashBody=Price2Calc*Volume2Calc
		# 佣金
		CommissionFee=5 if CashBody*CommissionRate<5 else CashBody*CommissionRate
		# 印花税费=卖出成交额*0.001
		StampFee=CashBody*0.001 if Direction_Order==0 else 0
		# 过户费，仅上海股票
		if cm.GetExchangeByCode(Code_Order)=='SHSE':
			TransferFee=1 if Price2Calc/1000<1 else Volume2Calc/1000
		else:
			TransferFee=0
		# 所有费用
		Fee=CommissionFee+StampFee+TransferFee
		# 加减过Fee的CashBody
		CashCalc=CashBody+Fee if Direction_Order==1 else CashBody-Fee
		# 返回结果
		return {'CashBody':CashBody,'Fee':Fee,'CashCalc':CashCalc,'CommissionFee':CommissionFee,'StampFee':StampFee,'TransferFee':TransferFee}














if __name__=='__main__':
	import Market
	Mkt = Market.MktSliNow()
	AddPar = {
		"ExchangeServerHost": "127.0.0.1",
		"ExchangeServerPort": 9501,
		"MaxConnnectTryTime": 100,
		"WaitTimeAfterTryConnect": 2
	}
	Account=Account("Usr","Pwd",AddPar,MktSliNow=Mkt)
	Account.ConnectAndLogin()
	Order = {'Code': '000001.SZSE', 'Direction': 1, 'Price': 9, 'Volume': 300, 'AddPar': {}}
	while not Account.CheckConnection():
		time.sleep(2)
	# 清除数据
	[Account.DelOrderByID(x) for x in Account.GetOrderList()]
	[Account.DelOrderRecByID(x) for x in Account.GetAllOrderList()]
	[Account.DelPositionByCode(x) for x in Account.GetPositionList()]
	Account.UpdateCashInfo({"Cash":1000000,"CashA":500000,"CashF":500000})
	Account.AddPosition("000002.SZSE")
	Account.UpdatePositionByCode("000002.SZSE",{"Vol":1000,"VolA":1000})
	# 开始测试
	Account.GetCashInfo()
	# 全部成交:买入
	Order = {'Code': '000001.SZSE', 'Direction': 1, 'Price': 0, 'Volume': 100, 'AddPar': {}}
	Account.PlaceOrder(**Order)
	# 全部成交:卖出
	Order = {'Code': '000002.SZSE', 'Direction': 0, 'Price': 0, 'Volume': 100, 'AddPar': {}}
	Account.PlaceOrder(**Order)
	# 部分成交:买入
	Order = {'Code': '000001.SZSE', 'Direction': 1, 'Price': 0, 'Volume': 600, 'AddPar': {}}
	Account.PlaceOrder(**Order)
	# 部分成交：卖出
	Order = {'Code': '000002.SZSE', 'Direction': 0, 'Price': 0, 'Volume': 600, 'AddPar': {}}
	Account.PlaceOrder(**Order)
	# 撤单
	time.sleep(5)
	Account.CancelOrder(Account.GetOrderList()[0])
	while 1:
		time.sleep(21)

