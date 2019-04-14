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


# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['Code','Vol','VolA','VolF','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','AddPar']
# 冻结资金明细
CASHFDETIAL_INDEX=['ID','Reason','Amt','Body','Fee']
ACCOUNTPAR_DAFAULT={'CommissionRate':0,'Slippage':0}
BUFFSIZE=1024 #接收消息缓存区大小，如果以后传的消息多了会修改

class Account(object):
	# 初始化,账户持仓信息中暂时没考虑多空双向持仓
	def __init__(self,Usr=None,Pwd=None,AddPar=None,Type='Stock',AccPar=ACCOUNTPAR_DAFAULT,MktSliNow=None,ClientGui=None):
		global A
		ClientLogger.info("柜台账户初始化...")
		# 柜台信息
		self.AccountID=self.CreateAccountID()
		self.Usr=Usr
		self.Pwd=Pwd
		self.AddPar=AddPar
		# 业务信息
		self.Position=pd.DataFrame(index=POSITION_INDEX)
		self.Order=pd.DataFrame(index=ORDER_INDEX)
		self.OrderRec=pd.DataFrame(index=ORDER_INDEX)
		self.CashInfo={'Cash':0,'InitCash':0,'CashA':0,'CashF':0,'CashFDetial':pd.DataFrame(index=CASHFDETIAL_INDEX)}
		# self.CashInfo=self.SetCashInfoValue('',[0,0,0,0,pd.DataFrame(index=CASHFDETIAL_INDEX)])
		self.AccPar=AccPar # 柜台账户参数数据，如账户手续费，保证金等数据
		self.MktSliNow=MktSliNow # 当前行情切片，作为一个外部数据源供柜台模块引用
		# 连接信息
		self.ConnectionClient=None
		self.ConnectState=0
		self.LogInState=0
		# Gui信息
		self.ClientGui=ClientGui
		# 开始连接服务器
		ret,msg=self.Connect(AddPar)
		ClientLogger.info("连接结果:{},{}".format(ret,msg))
		# 连接成功，开始登录和监听接收消息
		if ret==1:
			# 开启监听服务器回报的线程
			# MsgRecThread = multiprocessing.Process(target=RecMsg)
			MsgRecThread = threading.Thread(target=self.RecMsg)
			# 子线程为守护线程
			MsgRecThread.daemon = True
			MsgRecThread.start()
			ClientLogger.debug("客户端消息监听线程启动")
			# 开始发送登录请求
			ret,msg=self.LogIn(Usr, Pwd)
			ClientLogger.debug("登录请求发送结果:{},{}".format(ret,msg))

	# 接收消息
	def RecMsg(self):
		Lock = threading.Lock()
		Msg = ''
		while True:
			try:
				RecData = self.ConnectionClient.recv(BUFFSIZE).decode('utf-8')
				ClientLogger.debug("读取缓冲区数据:{}".format(RecData))
			except:
				ClientLogger.warning("接收缓冲区数据失败!")
				if self.ConnectState==1:
					self.ReConnect()
				else:
					exit(0)
			if RecData == '': self.Exit()
			Msglist,Msg=GeneralMod.AnalyzeMsg(Msg,RecData)
			for AimMsg in Msglist:
				try:
					Lock.acquire()
					self.DealRecMsg(AimMsg)
					Lock.release()
				except Exception as e:
					Lock.release()
					ClientLogger.error("处理消息出错:{},{}".format(AimMsg,e))


	# 处理接收消息的函数
	def DealRecMsg(self,Msg):
		ClientLogger.debug("处理消息:{}".format(Msg))
		# 测试打印字符串
		if Msg['MsgType']=="Print":
			print('处理接收消息的线程打印：{}'.format(Msg))
		# 退出
		if Msg['MsgType']=="Exit":
			self.Exit()
		# 登录成功回报
		if Msg['MsgType']=="LogInReturn":
			# multiprocessing.Lock().acquire()
			self.LogInState=1
			# multiprocessing.Lock().release()
			ClientLogger.info("登录成功:{}".format(Msg))
		# 下单回报
		if Msg['MsgType'] == "OrderReturn":
			self.DealOrderRet(Msg['OrderID'], Msg["ret"], Msg["msg"],Msg["OrderTime"])
			pass
		# 成交回报
		if Msg['MsgType']=="TransactionReturn":
			self.DealMatchRet(Msg['OrderID'],Msg["MatchInfo"],Msg["MatchTime"])
		# 撤单回报
		if Msg['MsgType']=="CancelOrderReturn":
			self.DealCancelOrderRet(Msg['OrderID'], Msg["ret"], Msg["msg"],Msg["CancelTime"])

	# 退出
	def Exit(self):
		pass

	# 生成柜台编号
	def CreateAccountID(self):
		return str(uuid.uuid1())

	# 柜台连接服务器登录
	def LogIn(self,Usr,Pwd):
		Msg={
			"MsgType":"LogIn",
			"Usr": Usr,
			"Pwd":Pwd,
			"AccountID":self.AccountID
		}
		ClientLogger.info("发送登录请求:{}".format(Msg))
		ret,msg=self.SendMsg(Msg)
		if ret==1:
			return 1,"登录请求发送成功"
		else:
			return 1, "登录请求发送失败"

	# 发送消息
	def SendMsg(self,Msg):
		Msg = GeneralMod.MakeSendMsg(Msg)
		self.ConnectionClient.send(str(Msg).encode('utf-8'))
		ClientLogger.debug("成功发送消息:{}".format(Msg))
		return 1,"发送成功"

	# 实盘账户初始化之后会连接柜台，获取交易参数等
	def Connect(self,AddPar):
		if AddPar["ExchangeServerHost"] !='':
			ConnectionClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			for TryTime in range(AddPar["MaxConnnectTryTime"]):
				try:
					ClientLogger.info("开始连接:{},{},第{}/{}次尝试...".format(AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"],TryTime+1,AddPar["MaxConnnectTryTime"]))
					ConnectionClient.connect((AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"]))
					self.CounterType = 'XXCounter'
					self.ConnectState=1
					self.ConnectionClient=ConnectionClient
					return 1,"连接成功"
				except:
					ClientLogger.warning("连接失败:{},{},等待{}s后重新连接...".format(AddPar["ExchangeServerHost"], AddPar["ExchangeServerPort"],AddPar["WaitTimeAfterTryConnect"]))
					time.sleep(AddPar["WaitTimeAfterTryConnect"])
			return 0, "连接失败"

	# 断连
	def DisConnect(self):
		self.ConnectionClient.close()
		self.ConnectionClient = None
		self.ConnectState = 0
		self.LogInState = 0
		ClientLogger.debug("断连成功")

	# 重连
	def ReConnect(self):
		self.DisConnect()
		ClientLogger.info("开始重新连接...")
		ret,msg=self.Connect(self.AddPar)
		if ret==1:
			ClientLogger.info("重连成功")
			ret,msg=self.LogIn(self.Usr,self.Pwd)
			ClientLogger.debug("登录请求发送结果:{},{}".format(ret,msg))
			if ret==1:self.RecMsg()
		else:
			exit(0)

	# 检查连接登录状态
	def CheckConnection(self):
		if self.ConnectState==0:
			return 0,"未连接服务器"
		elif self.LogInState==0:
			return 0,"未登录"
		return 1,"账户连接登录正常"

	# 刷新账户信息
	def Refresh(self):
		# 更新持仓信息
		if self.CounterType=='BackTestCounter':
			TempIndex=self.MatchingSys.Account.index(self)
			self.Position=self.MatchingSys.Position[TempIndex]
			self.Order=self.MatchingSys.Order[TempIndex]
			self.AccountAddPar=self.MatchingSys.AccountAddPar[TempIndex]
		elif self.CounterType=='XXCounter':
			pass
		# Log.info('Refresh Position Success!')
		# 以下是测试用
		# if '000001.SZSE' in self.Position.columns:
			# Log.debug(list(self.Position['000001.SZSE']))

	# 获取持仓信息
	def GetPositionByCode(self,Code,Item=POSITION_INDEX):
		if type(Item) is str:
			if Code in self.Position.columns:
				return self.Position[Code].loc[Item]
		if type(Item) is not list:Item=[Item]
		if Code in self.Position.columns:
			return list(self.Position[Code].loc[Item])
		else:
			return [None]*len(Item)

	# 获取订单数据
	def GetOrderByID(self,OrderID,Item=ORDER_INDEX):
		if type(Item) is str:
			if OrderID in self.OrderRec.columns:
				return self.OrderRec[OrderID].loc[Item]
		if type(Item) is not list:Item=[Item]
		if OrderID in self.OrderRec.columns:
			return list(self.OrderRec[OrderID].loc[Item])
		else:
			return [None]*len(Item)

	# 生成订单下单时间
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 检查订单状态（如订单全部成交则需要删除等）
	def CheckOrderByID(self,OrderID):
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
			self.SetOrderValue(OrderID,"State","Error")
			# 清除订单
			self.DelOrderByID(OrderID)

		return 1,''

	# 删除订单
	def DelOrderByID(self,OrderID):
		if OrderID in self.Order.columns:
			self.Order.drop(labels=OrderID, axis=1, inplace=True)
			ClientLogger.info("清除订单成功:{}".format(OrderID))

	# 删除持仓
	def DelPositionByCode(self,Code):
		if Code in self.Position.columns:
			self.Position.drop(labels=Code, axis=1, inplace=True)
			ClientLogger.info("清除持仓成功:{}".format(Code))

	# 检查持仓数据（如无效持仓需要清理等）
	def CheckPositionByCode(self,Code):
		ClientLogger.debug("检查持仓信息:{}".format(Code))
		# 持仓数据
		Vol=self.GetPositionByCode(Code,'Vol')
		# 判断是否全部成交
		if Vol==0:
			# 清除持仓
			self.DelPositionByCode(Code)
		elif Vol==None:
			# 本来就没持仓了
			pass
		return 1,''

	# 根据成交回报处理OrderList
	def DealMatchRetInOrderList(self,OrderID,MatchInfo,CalcRet):
		ClientLogger.debug("更新订单列表:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,AddPar_Old=self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Old==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody,Fee,CashCalc=CalcRet["CashBody"],CalcRet["Fee"],CalcRet["CashCalc"]
		# 开始处理
		# 计算新的订单记录的字段
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,AddPar=Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,AddPar_Old
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
		# 成交均价=（此前成交总价+本次成交金额（计算了费用的））/总已成量
		AvgMatchingPrice=(VolumeMatched_Old*AvgMatchingPrice_Old+CashCalc)/VolumeMatched
		# 冻结资金计算
		if Direction==1:
			AddPar["CashFrozen"] = AddPar["CashFrozen"] - CashCalc
			AddPar["FeeFrozen"] = AddPar["FeeFrozen"] - Fee
			AddPar["FeeConfirm"] = AddPar["FeeConfirm"]+Fee if "FeeConfirm" in AddPar else Fee
		elif Direction==0:
			AddPar["VolumeFrozen"]=AddPar["VolumeFrozen"]-VolumeMatched
			AddPar["FeeFrozen"] = AddPar["FeeFrozen"] - Fee
			AddPar["FeeConfirm"] = AddPar["FeeConfirm"] + Fee if "FeeConfirm" in AddPar else Fee
		self.SetOrderValue(OrderID,"AddPar",AddPar)
		# 回写数据到Order及OrderRec
		self.SetOrderValue(OrderID,'',[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,AddPar])
		# 检查订单状态（如订单全部成交则需要取消等）
		ret,msg=self.CheckOrderByID(OrderID)
		ClientLogger.debug("订单数据:{}".format(self.GetOrderByID(OrderID)))
		return 1,''

	# 根据成交回报处理PositionList
	def DealMatchRetInPositionList(self,OrderID,MatchInfo,CalcRet):
		ClientLogger.debug("更新持仓列表:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,VolumeMatched_Order,State_Order,AvgMatchingPrice_Order,OrderTime_Order,OrderNum_Order,Mkt_Order,Account_Order,Config_Order=self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody, Fee, CashCalc = CalcRet["CashBody"], CalcRet["Fee"], CalcRet["CashCalc"]
		# 判断是否已有持仓
		if Code_Order in list(self.Position.columns):
			Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position=self.GetPositionByCode(Code_Order)
		else:
			Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position=[Code_Order,0,0,0,0,0,0,0,0,0,'CNY',cm.GetExchangeByCode(Code_Order),self,{}]
		# 初始化持仓字段
		Code,Vol,VolA,VolF,StockActualVol,AvgCost,PriceNow,MktValue,FloatingProfit,ProfitRatio,Currency,Mkt,Account,Config=Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position
		# 计算持仓字段
		# 主要分多空
		if Direction_Order==1:
			Vol=Vol_Position+VolumeMatching
			VolA=VolA_Position # 股票T+1，可用量不变
			Config["FrozenToday"]=Config_Position["FrozenToday"]+VolumeMatching if "FrozenToday" in Config_Position else VolumeMatching
			VolF=VolF_Position+VolumeMatching
			StockActualVol=StockActualVol_Position
			AvgCost=(AvgCost_Position*Vol_Position+CashCalc)/Vol
		elif Direction_Order==0:
			Vol=Vol_Position-VolumeMatching
			VolA=VolA
			VolF=VolF_Position-VolumeMatching
			StockActualVol=StockActualVol_Position
			# 卖出平均成本=0 if 持仓=0 else （旧的平均成本*旧的持仓量-卖出收回资金）/新持仓量
			AvgCost=0 if Vol==0 else (AvgCost_Position*Vol_Position-CashCalc)/Vol
		# 回写数据到持仓数据中
		# 因为其他的字段都和实时行情有关，回写完毕后重新调用一个函数即可
		self.SetPositionValue(Code,'',[Code,Vol,VolA,VolF,StockActualVol,AvgCost,PriceNow,MktValue,FloatingProfit,ProfitRatio,Currency,Mkt,Account,Config])
		# 重新计算实时持仓盈亏
		ret,msg=self.CalcPositionRealTimeValueByCode(Code)
		# 检查持仓信息（如无效持仓清除等）
		ret,msg=self.CheckPositionByCode(Code)
		return 1,''

	# 更新资金信息CashInfo 
	def DealMatchRetInCashInfo(self,OrderID,MatchInfo,CalcRet):
		ClientLogger.debug("更新资金信息:{},{}".format(OrderID, MatchInfo))
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,VolumeMatched_Order,State_Order,AvgMatchingPrice_Order,OrderTime_Order,OrderNum_Order,Mkt_Order,Account_Order,Config_Order=self.GetOrderByID(OrderID)
		# 成交数据
		# PriceMatching=MatchInfo['PriceMatching']
		# VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		# CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		# CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		CashBody, Fee, CashCalc = CalcRet["CashBody"], CalcRet["Fee"], CalcRet["CashCalc"]
		# 资金数据
		Cash_Old=self.GetCashInfoByItem('Cash')
		InitCash_Old=self.GetCashInfoByItem('InitCash')
		CashA_Old=self.GetCashInfoByItem('CashA')
		CashF_Old=self.GetCashInfoByItem('CashF')
		# 开始计算
		# 买入计算
		if Direction_Order==1:
			Cash=Cash_Old-CashCalc
			InitCash=InitCash_Old
			CashA=CashA_Old
			CashF=CashF_Old-CashCalc
		elif Direction_Order==0:
			Cash=Cash_Old+CashCalc
			InitCash=InitCash_Old
			CashA=CashA_Old+CashCalc
			# 卖出的话冻结资金要减去冻结的费用
			CashF=CashF_Old-Fee
		# 回写数据
		# self.CashInfo['Cash']=Cash
		# self.CashInfo['InitCash']=InitCash
		# self.CashInfo['CashA']=CashA
		# self.CashInfo['CashF']=CashF
		self.SetCashInfoValue(['Cash','InitCash','CashA','CashF'],[Cash,InitCash,CashA,CashF])
		ClientLogger.debug("资金信息:{}".format(self.GetCashInfoByItem(['Cash','InitCash','CashA','CashF'])))
		return 1,''

	# 计算实时持仓价值
	def CalcPositionRealTimeValueByCode(self,Code):
		ClientLogger.debug("计算实时持仓价值:{}".format(Code))
		if Code not in self.Position.columns:return 0,'无效Code！'
		# 市场数据
		Price=self.MktSliNow.GetDataByCode(Code,'Price')
		# 更新数据
		PriceNow=Price
		MktValue=Price*self.GetPositionByCode(Code,'Vol')
		FloatingProfit=(Price-self.GetPositionByCode(Code,'AvgCost'))*self.GetPositionByCode(Code,'Vol')
		ProfitRatio=(Price-self.GetPositionByCode(Code,'AvgCost'))/self.GetPositionByCode(Code,'AvgCost') if self.GetPositionByCode(Code,'AvgCost')!=0 else 0
		self.SetPositionValue(Code,['PriceNow','MktValue','FloatingProfit','ProfitRatio'],[PriceNow,MktValue,FloatingProfit,ProfitRatio])
		ClientLogger.debug("持仓数据:{}".format(self.GetPositionByCode(Code)))
		return 1,''
		
	# 处理订单成交回报
	def DealMatchRet(self,OrderID,MatchInfo,MatchTime):
		ClientLogger.info("处理成交回报:{},{},{}".format(OrderID,MatchInfo,MatchTime))
		# 计算资金费用等
		CalcRet=self.CalcOrderFee(OrderID,MatchInfo)
		# 更新订单列表
		ret,msg=self.DealMatchRetInOrderList(OrderID,MatchInfo,CalcRet)
		# 更新持仓列表
		ret,msg=self.DealMatchRetInPositionList(OrderID,MatchInfo,CalcRet)
		# 更新资金列表
		ret,msg=self.DealMatchRetInCashInfo(OrderID,MatchInfo,CalcRet)
		return 1,''

	# 账户下单
	def PlaceOrder(self,Code,Direction,Price,Volume,AddPar=None):
		# 检查连接登录状态等
		ret,msg=self.CheckConnection()
		if ret==0:return ret,msg
		# 开始下单
		ClientLogger.info("账户下单:{}".format([Code,Direction,Price,Volume,AddPar]))
		Order={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'AddPar':AddPar}
		# 验单
		MktInfo={'Price_LimitUp':self.MktSliNow.GetDataByCode(Code,'Price_LimitUp'),'Price_LimitDown':self.MktSliNow.GetDataByCode(Code,'Price_LimitDown')}
		ret,msg=self.CheckNewOrder(Order,MktInfo)
		ClientLogger.info("验单结果:{},{}".format(ret,msg))
		if ret==0:
			return ret,msg,''
		else:
			# 记录订单
			OrderID=self.LogNewOrder(Order)
			# 资金冻结
			ret,msg=self.FrozenNewOrder(OrderID)
			# 发送到交易所撮合
			ret,msg=self.SendNewOrderToMatch(OrderID)
		return ret,msg,OrderID

	# 订单校验
	# 验单进行资金冻结等
	# 需求参数：账户信息，订单信息(其中账户信息，参照CTP，可以自己进行订单验证)，验单需要的其他信息，如涨跌停价格
	# 主要内容：1.判断价格是否正确（涨跌停以内）;2.判断可用资金和可用量是否充足。
	def CheckNewOrder(self,Order,MktInfo):
		ClientLogger.debug("柜台验单:{},{}".format(Order,MktInfo))
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
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
			PositionVolume=(self.GetPositionByCode(Code,'Vol') if self.GetPositionByCode(Code,'Vol')!=None else 0)
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
			if Volume*Price2Frozen*(1+CommissionRate)>self.GetCashInfoByItem('CashA'):
				ret=0
				msg='可用资金不足，订单无效'
				return ret,msg
		elif Direction==0:
			if Volume>(self.GetPositionByCode(Code,'VolA') if self.GetPositionByCode(Code,'VolA')!=None else 0):
				ret=0
				msg='可用持仓不足，订单无效'
				return ret,msg
		return 1,'订单有效'

	# 冻结资金持仓等
	# 验单通过的订单进行冻结资金的操作
	# 这里没有数据锁，可能出现验单通过实际冻结的时候却不足的问题吗？
	def FrozenNewOrder(self,OrderID):
		Code,Volume,Direction=self.GetOrderByID(OrderID,['Code','Volume','Direction'])
		ClientLogger.debug("冻结资金:{},{}".format(OrderID,[Code,Volume,Direction]))
		# 计算费用
		FeeCalc = self.CalcOrderFee(OrderID)
		CashBody, Fee, CashCalc = FeeCalc['CashBody'], FeeCalc['Fee'], FeeCalc['CashCalc']
		# 买入冻结资金
		if Direction==1:
			self.SetCashInfoValue('CashA', self.GetCashInfoByItem('CashA') - CashCalc)
			self.SetCashInfoValue('CashF', self.GetCashInfoByItem('CashF') + CashCalc)
			# 在订单中进行记录
			AddPar=self.GetOrderByID(OrderID,"AddPar")
			AddPar["CashFrozen"]=CashCalc
			AddPar["FeeFrozen"]=Fee
			AddPar["CashFrozenWhenOrdering"] = CashCalc
			AddPar["CashBodyFrozenWhenOrdering"] = CashBody
			AddPar["FeeFrozenWhenOrdering"] = Fee
			self.SetOrderValue(OrderID,"AddPar",AddPar)
		elif Direction==0:
			# 卖出冻结手续费
			self.SetCashInfoValue('CashA', self.GetCashInfoByItem('CashA') - Fee)
			self.SetCashInfoValue('CashF', self.GetCashInfoByItem('CashF') + Fee)
			# 更新持仓
			self.SetPositionValue(Code,["VolA"],self.GetPositionByCode(Code,"VolA")-Volume)
			self.SetPositionValue(Code, ["VolF"], self.GetPositionByCode(Code, "VolF") + Volume)
			# 在订单中进行记录
			AddPar=self.GetOrderByID(OrderID,"AddPar")
			AddPar["VolumeFrozen"]=Volume
			AddPar["FeeFrozen"] = Fee
			AddPar["VolumeFrozenWhenOrdering"]=Volume
			AddPar["FeeFrozenWhenOrdering"] = Fee
			self.SetOrderValue(OrderID,"AddPar",AddPar)
		return 1,'冻结资金持仓成功！'

	# 将订单资金等解冻
	def UnFrozenOrder(self,OrderID):
		Code, Volume, VolumeMatched,Direction,AddPar = self.GetOrderByID(OrderID, ['Code', 'Volume','VolumeMatched', 'Direction','AddPar'])
		ClientLogger.debug("资金解冻:{},{}".format(OrderID, [Code, Volume, VolumeMatched,Direction,AddPar]))
		# 买入解冻资金
		if Direction==1:
			CashFrozen,FeeFrozen=AddPar["CashFrozen"],AddPar["FeeFrozen"]
			self.SetCashInfoValue('CashA', self.GetCashInfoByItem('CashA') - CashFrozen)
			self.SetCashInfoValue('CashF', self.GetCashInfoByItem('CashF') + CashFrozen)
			AddPar["CashFrozen"], AddPar["FeeFrozen"]=0,0
			self.SetOrderValue(OrderID,"AddPar",AddPar)
		elif Direction==0:
			VolumeFrozen,FeeFrozen=AddPar["VolumeFrozen"],AddPar["FeeFrozen"]
			self.SetPositionValue(Code,["VolA"],self.GetPositionByCode(Code,"VolA")+VolumeFrozen)
			self.SetPositionValue(Code, ["VolF"], self.GetPositionByCode(Code, "VolF") - VolumeFrozen)
			self.SetCashInfoValue('CashA', self.GetCashInfoByItem('CashA') - FeeFrozen)
			self.SetCashInfoValue('CashF', self.GetCashInfoByItem('CashF') + FeeFrozen)
			AddPar["VolumeFrozen"], AddPar["FeeFrozen"]=0,0
			self.SetOrderValue(OrderID, "AddPar", AddPar)
		return 1,'资金持仓解冻成功！'

	# 记录新订单，将新订单加入订单记录中并生成订单id 
	def LogNewOrder(self,Order):
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# 生成订单编号
		OrderID=self.CreateOrderID()
		# 记录订单
		ClientLogger.info("记录订单:{},{}".format(OrderID,Order))
		self.SetOrderValue(OrderID,'',[Code,Direction,Price,Volume,0,'SendToMatch',0,self.CreateOrderTime(),OrderID,cm.GetExchangeByCode(Code),self,AddPar])
		return OrderID

	# 生成订单ID
	def CreateOrderID(self):
		return str(uuid.uuid1())
	
	# 发送新订单到“虚拟交易所”进行撮合
	def SendNewOrderToMatch(self,OrderID):
		Code,Direction,Price,Volume,AddPar=self.GetOrderByID(OrderID,['Code','Direction','Price','Volume','AddPar'])
		Msg={
			"MsgType": "PlaceOrder",
			"Order": {"Code": Code, "Direction": Direction, "Price": Price, "Volume": Volume, "AddPar": AddPar},
			"OrderID": OrderID
		}
		ClientLogger.info("发送下单请求:{}".format(Msg))
		self.SendMsg(Msg)
		return 1,"发送成功"

	# 计算订单手续费等
	def CalcOrderFee(self,OrderID,MatchInfo=None):
		ClientLogger.debug("计算订单手续费:{},{}".format(OrderID,MatchInfo))
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,VolumeMatched_Order,State_Order,AvgMatchingPrice_Order,OrderTime_Order,OrderNum_Order,Mkt_Order,Account_Order,Config_Order=self.GetOrderByID(OrderID)	
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
		# 市场数据
		Price_LimitUp=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitUp')
		Price_LimitDown=self.MktSliNow.GetDataByCode(Code_Order,'Price_LimitDown')
		# 开始计算
		# 根据计算时机不同而不同，可能在下单冻结计算或在成交清算计算
		if MatchInfo!=None:
			# 根据成交回报计算交易金额
			Price2Calc=MatchInfo['PriceMatching']
			Volume2Calc=MatchInfo['VolumeMatching']
		elif Price_Order==0 and Direction_Order==1:
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

	# 更新订单状态的函数
	def SetOrderValue(self,OrderID,Item,Value):
		if Item=='':Item=ORDER_INDEX
		if OrderID not in self.Order.columns:
			self.Order[OrderID] = Value
			self.OrderRec[OrderID] = Value
		else:
			self.Order[OrderID][Item]=Value
			self.OrderRec[OrderID][Item] = Value
		ClientLogger.debug("更新订单状态:{}".format(self.GetOrderByID(OrderID)))

	# 更新持仓状态的函数
	def SetPositionValue(self,Code,Item,Value):
		if Item=='':Item=POSITION_INDEX
		if Code not in self.Position.columns:
			self.Position[Code]=Value
		else:
			self.Position[Code][Item] = Value
		ClientLogger.debug("更新持仓状态:{}".format(self.GetPositionByCode(Code)))

	# 更新资金状态的函数
	def SetCashInfoValue(self,Item,Value):
		if Item=="":Item=['Cash','InitCash','CashA','CashF','CashFDetial']
		if type(Item) is not list:Item=[Item]
		if type(Value) is not list: Value = [Value]
		for x in Item:
			self.CashInfo[x]=Value[Item.index(x)]

	# 查询资金状态的函数
	def GetCashInfoByItem(self,Item=['Cash','InitCash','CashA','CashF','CashFDetial']):
		if type(Item) is str:return self.CashInfo[Item]
		if type(Item) is not list: Item = [Item]
		Value=[self.CashInfo[x] for x in Item]
		return Value



	# 处理订单回报
	def DealOrderRet(self,OrderID,ret,msg,OrderTime):
		ClientLogger.info("处理订单回报:{},{},{},{}".format(OrderID,ret,msg,OrderTime))
		if ret==1:
			self.SetOrderValue(OrderID,["State","OrderTime"],["WaitToMatch",OrderTime])

	# 获取订单列表
	def GetOrderList(self):
		return list(self.Order.columns)

	# 检验撤单是否有效
	def CheckCancelOrder(self,OrderID):
		if OrderID in self.GetOrderList():
			return 1
		return 0

	# 撤单函数
	def CancelOrder(self,OrderID):
		ClientLogger.info("撤销订单:{}".format(OrderID))
		# 验单
		if self.CheckCancelOrder(OrderID):
			self.SendOrderToCancel(OrderID)

	# 发送撤单信息
	def SendOrderToCancel(self,OrderID):
		ClientLogger.info("发送测单信息:{}".format(OrderID))
		Msg={
			"MsgType":"CancelOrder",
			"OrderID":OrderID
		}
		ret,msg=self.SendMsg(Msg)

	# 处理撤单回报
	def DealCancelOrderRet(self,OrderID,ret,msg,CancelTime):
		ClientLogger.info("处理撤单回报:{},{},{},{}".format(OrderID,ret,msg,CancelTime))
		if ret==1:
			AddPar=self.GetOrderByID(OrderID,"AddPar")
			AddPar["CancelTime"]=CancelTime
			self.SetOrderValue(OrderID,["State","AddPar"],["Canceled",AddPar])
			# 检查订单状态，将订单冻结的资金等归还和清除订单
			self.CheckOrderByID(OrderID)




if __name__=='__main__':
	import Market
	Mkt = Market.MktSliNow()
	AddPar = {
		"ExchangeServerHost": "127.0.0.1",
		"ExchangeServerPort": 9501,
		"MaxConnnectTryTime": 100,
		"WaitTimeAfterTryConnect": 2
	}
	Account=Account("Usr","Pwd",AddPar)
	Order = {'Code': '000001.SZSE', 'Direction': 1, 'Price': 9, 'Volume': 300, 'AddPar': {}}
	Account.PlaceOrder(**Order)
	while 1:
		time.sleep(5)