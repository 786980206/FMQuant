# -*- coding: utf-8 -*-

import pandas as pd

# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['Code','Vol','VolA','VolF','StockActualVol','Avgcost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']

ACCOUNTPAR_DAFAULT={'CostRatio':0}

################################################# 模块导入 ##############################################################
## 导入所需模块
import sys
import os
import time
from enum import Enum
import datetime
import pandas as pd
import math
# import PushMod # 数据模块
import TradeMod # 交易模块
# import StrategyMod.StrategyMod as StrategyMod # 策略模块
import EventMod
import GeneralMod
Log=GeneralMod.Log()

################################################ 变量定义 ###############################################################
# 编辑常量
# 这里之后可能会加上多空持仓方向
POSITION_INDEX=['Code','Vol','VolA','VolFrozen','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
ORDER_REC_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
DEAL_REC_INDEX=['MatchingTime','Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','MatchingVol','OrderTime','OrderNum','CloseProfit','Mkt','Account','Config']
CASH_REC_INDEX=["Time","TotalValue","Cash","CashAvailable","CashFrozen","InitCash","SecurityValue"]
# 枚举常量
# 货币枚举
class CURRENCY(Enum):
	UNK=0 # Unkonw
	CNY='CNY'
	USD='USD'
	HKD='HKD'
	UKB='UKB'
# 市场枚举
class MARKET(Enum):
	UNK=0
	SHSE=1
	SZSE=2
	CFFEX=3
	SHFE=4
	DCE=5
	CZSE=6
	HKEX=7
# 时间枚举
class TIME_INTERVAL(Enum):
	UNK=0
	SEC_01=1
	MIN_01=60
	DAY_01=86400
# 时间枚举
class DIRECTION(Enum):
	LONG_BUY=1
	LONG_SELL=0
	SHORT_BUY=-1
	SHORT_SELL=2
# 状态枚举
class ORDER_STATE(Enum):
	UNK=0
	WAIT_TO_MATCH='WaitToMatch'
	NOT_MATCHED='NotMatched'
	PART_MATCHED='PartMatched'
	ALL_MATCHED='AllMatched'
	ORDER_CANCEL='OrderCancel'
# 订单取消枚举
class ORDER_CANCEL_REASON(Enum):
	UNK=0
	AUTO_CANCEL_EVERYDA='AutoCancelEveryday'
	CASH_AVAILABLE_NOT_ENOUGH='CashAvailable not enough!'
	VOL_AVAILABLE_NOT_ENOUGH='VolA not enough!'
	NO_VOL_FOR_TRADING_NOW='No Vol for trading now!'
	WRONG_ORDER_PRICE='Wrong order price!'
	PRICE_NOT_MATCHED='Price Not Matched!'
# 订单撮合返回值枚举
class MATCHING_RET(Enum):	
	PRICE_NOT_MATCHED='Price Not Matched!'
	NO_VOL_FOR_TRADING_NOW='No Vol4Trd Now!'
# 账户参数枚举
class ACCOUNT_CONFIG(Enum):
	CASH='Cash'
	INIT_CASH='InitCash'
	CASH_AVAILABLE='CashAvailable'
	CASH_FROZEN='CashFrozen'
	TOTAL_VALUE='TotalValue'
	SECURITY_VALUE='SecurityValue'

################################################ 类定义 ###############################################################
class Exchange(object):
	def __init__(self,MktSliNow=None):
		self.OrderPool=pd.DataFrame(index=ORDER_INDEX)
		self.MktSliNow=MktSliNow

	# 获取订单数据
	def GetOrderByID(self,OrderID,Item=ORDER_INDEX):
		if type(Item) is not list:Item=[Item]
		if OrderID in self.OrderPool.columns
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
			self.OrderPool.drop(label=OrderID,axis=1,inplace=True)
		return 1,''


	# 处理从柜台新推过来的订单数据
	def DealNewOrder(self,OrderID,Order):
		# 加入订单池
		self.OrderPool[OrderID]=Order
		# 开始撮合
		MktInfo={'Price4Trd':self.MktSliNow.GetDataByCode(Order[0],'Price'),'Volume4Trd':self.MktSliNow.GetDataByCode(Order[0],'Volume4Trd')}
		ret,msg,MatchInfo=self.MatchOrder(OrderID,MktInfo)
		# 判断是否成交
		if MatchInfo['VolumeMatched']==0:
			return 1,'无成交'
		# 处理撮合结果
		# OrderPool更新
		ret,msg=self.DealMatchRetInOrderPool(OrderID,MatchInfo)
		# 市场行情切片也要处理撮合结果（扣除成交量等）
		self.MktSliNow.DealMatchRet(self.GetOrderByID(OrderID),MatchInfo)
		# 通知柜台处理成交回报
		# 生成成交时间
		MatchTime=self.CreateMatchTime()
		self.OrderPool[OrderID].loc['Account'].DealMatchRet(OrderID,MatchInfo,MatchTime)
		return ret,msg

	# 处理撮合结果
	def DealMatchRetInOrderPool(self,OrderID,MatchInfo):
		# 订单数据
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		CostRatio=self.OrderPool[OrderID].loc['Account'].AccPar['CostRatio']
		# 成交金额计算
		CashMatching=PriceMatching*VolumeMatching*(1+CostRatio) if Direction==1 else PriceMatching*VolumeMatching*(1-CostRatio)
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
		# 柜台数据
		CostRatio=self.OrderPool[OrderID].loc['Account'].AccPar['CostRatio']
		# 撮合设置数据（暂时先放到柜台的参数中）
		Slippage=self.OrderPool[OrderID].loc['Account'].AccPar['Slippage']
		# 计算订单未成交量
		VolumeNotMatched=Volume-VolumeMatched
		# 开始撮合
		# 价格对比
		# 市价多单
		if Price==0 and Direction==1:
			PriceMatched=Price4Trd+Slippage
		# 限价多单
		elif (Price>=Price4Trd) and Direction==1:
			PriceMatched=Price4Trd
		# 市价平多
		elif Price==0 and Direction==0:
			PriceMatched=Price4Trd-Slippage
		# 限价平多
		elif Price<Price4Trd and Direction==0:
			PriceMatched=Price4Trd
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
		return 1,'',{'PriceMatching':PriceMatched,'VolumeMatching':VolumeMatched}

## 回测模块函数
if __name__=='__main__':
	pass
	# test
	#
