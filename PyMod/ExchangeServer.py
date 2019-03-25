# -*- coding: utf-8 -*-

import socket
import multiprocessing
import datetime
import pandas as pd
import json
import time
import uuid
import Market

# 常量定义
POSITION_INDEX=['Code','Vol','VolA','VolFrozen','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
BUFFSIZE=1024 #接收消息缓存区大小，如果以后传的消息多了会修改

# 接收消息
def RecMsg(cnn,ExchangeCore):
	Msg=''
	while True:
		RecData=cnn.recv(BUFFSIZE).decode('utf-8')
		Msg=Msg+RecData
		TempMsglist=Msg.split('|End')
		Msglist=TempMsglist[0:-1]
		Msg=TempMsglist[-1]
		for AimMsg in Msglist:
			if AimMsg[0:4]!='Msg:':continue
			AimMsg=AimMsg[4:]
			try:
				AimMsg=json.loads(AimMsg)
				DealRecMsg(AimMsg,ExchangeCore)
			except Exception as e:
				print(e)
				# print(AimMsg)

# 处理接收消息的函数
def DealRecMsg(Msg,ExchangeCore):
	if Msg['MsgType']=="Print":
		print('处理接收消息的线程打印：{}'.format(Msg))
	if Msg['MsgType']=="DealNewOrder":
		AccountID,Order=Msg['AccountID'],Msg['Order']
		ExchangeCore.DealNewOrder(Order,AccountID)


# 初始化
def Init():
	ExchangeCore=Exchange()
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('0.0.0.0',9501))
	s.listen(1)
	while True:
		cnn,addr=s.accept()
		print('{}:连接成功!'.format(datetime.datetime.now()))
		m=multiprocessing.Process(target=RecMsg,args=(cnn,ExchangeCore))
		# 子线程为守护线程
		m.daemon=True
		m.start()
		# 等待子线程结束
		m.join()
		cnn.close()
		print('{}:连接断开!'.format(datetime.datetime.now()))

################################################ 类定义 ###############################################################
class Exchange(object):
	def __init__(self,MktSliNow=None,OrderPool=None):
		self.OrderPool=OrderPool if OrderPool!=None else pd.DataFrame(index=ORDER_INDEX)
		self.MktSliNow=MktSliNow if MktSliNow!=None else Market.MktSliNow()
		self.Slippage=0

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

	# 判断订单状态（如订单全部成交则需要取消等）
	def CheckOrderByID(self,OrderID):
		# 订单数据
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=self.GetOrderByID(OrderID)
		# 判断是否全部成交
		if Volume==VolumeMatched and State=='AllMatched':
			# 清除订单
			self.OrderPool.drop(labels=OrderID,axis=1,inplace=True)
		return 1,''

	# 生成订单下单时间
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 记录新订单，将新订单加入订单记录中并生成订单id
	def LogNewOrder(self,Order,AccountID):
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# 生成订单编号
		OrderID=str(uuid.uuid1())
		# 记录订单
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,0,'WaitToMatch',0,self.CreateOrderTime(),OrderID,'Mkt',AccountID,AddPar]
		return OrderID


	# 处理从柜台新推过来的订单数据
	def DealNewOrder(self,Order,AccountID,MarkeSliNow=None):
		if MarkeSliNow==None:MarkeSliNow=self.MktSliNow
		# 订单数据
		Code, Direction,Price,Volume,AddPar=Order['Code'],Order['Direction'],Order['Price'],Order['Volume'],Order['AddPar']
		# 记录新订单
		OrderID=self.LogNewOrder(Order,AccountID)
		# 开始撮合
		MktInfo={'Price4Trd':MarkeSliNow.GetDataByCode(Code,'Price'),'Volume4Trd':MarkeSliNow.GetDataByCode(Code,'Volume4Trd')}
		ret,msg,MatchInfo=self.MatchOrder(OrderID,MktInfo)
		# 判断是否成交
		if MatchInfo['VolumeMatching']==0:
			return 1,'无成交'
		# 处理撮合结果
		# OrderPool更新
		ret,msg=self.DealMatchRetInOrderPool(OrderID,MatchInfo)
		# 市场行情切片也要处理撮合结果（扣除成交量等）
		MarkeSliNow.DealMatchRet(Code,MatchInfo)
		# 通知柜台处理成交回报
		# 生成成交时间
		MatchTime=self.CreateMatchTime()
		ret,msg=Account.DealMatchRet(OrderID,MatchInfo,MatchTime)
		return ret,msg,OrderID

	# 处理撮合结果
	def DealMatchRetInOrderPool(self,OrderID,MatchInfo):
		# 订单数据
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		CommissionRate=self.OrderPool[OrderID].loc['Account'].AccPar['CommissionRate']
		# 成交金额计算
		CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Old==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
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
		# 成交均价
		AvgMatchingPrice=(VolumeMatched_Old*AvgMatchingPrice_Old+CashMatching)/VolumeMatched
		# 回写数据到OrderPool
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config]
		# 检查订单状态（如订单全部成交则需要取消等）
		ret,msg=self.CheckOrderByID(OrderID)
		return 1,''


	# 撮合订单的函数
	# 需要用到订单数据，市场数据，柜台数据（费率等），其他撮合数据（如滑点，最大成交比例等）
	def MatchOrder(self,OrderID,MktInfo):
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
		elif Price<Price4Trd and Direction==0:
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


if __name__=='__main__':
		Init()