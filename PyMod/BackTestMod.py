#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'

################################################# 模块导入 ##############################################################
## 导入所需模块
import sys
import os
import time
from enum import Enum
from datetime import datetime
import pandas as pd
import math
import PushMod # 数据模块
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
class MatchingSys(object):
	def __init__(self,Strategy,EventEngine,MatchConfig):
		# 初始化，给策略账户绑定回测撮合系统
		# SubConfig=Config['SubConfig']
		# BackTestConfig=Config['BackTestConfig']
		self.IsRunning=True
		self.Account=[]
		self.Position=[]
		self.Order=[]
		self.OrderRec=[]
		self.DealRec=[]
		self.CashRec=[]
		self.AccountConfig=[]
		self.QuotationsNow=pd.DataFrame(columns=Strategy.QuoteDataConfig['CodeList'],index=MatchConfig['Fields'])
		self.Time=datetime.strptime(MatchConfig['StartTime'],'%Y-%m-%d %H:%M:%S')
		self.OrderNum=0 # 订单记录号
		for TempAccount in Strategy.Account:
			TempAccount.MatchingSys=self
			self.Account.append(TempAccount)
			self.Position.append(pd.DataFrame(index=POSITION_INDEX))
			self.Order.append(pd.DataFrame(index=ORDER_INDEX))
			self.OrderRec.append(pd.DataFrame(index=ORDER_REC_INDEX))
			self.AccountConfig.append({ACCOUNT_CONFIG.TOTAL_VALUE.value:MatchConfig['InitCash'],\
									   ACCOUNT_CONFIG.CASH.value:MatchConfig['InitCash'],\
									   ACCOUNT_CONFIG.INIT_CASH.value:MatchConfig['InitCash'],\
									   ACCOUNT_CONFIG.CASH_AVAILABLE.value:MatchConfig['InitCash'],\
									   ACCOUNT_CONFIG.CASH_FROZEN.value:0,\
									   ACCOUNT_CONFIG.SECURITY_VALUE.value:0,\
									   })
			self.DealRec.append(pd.DataFrame(index=DEAL_REC_INDEX))
			self.CashRec.append(pd.DataFrame(index=CASH_REC_INDEX))
		self.MatchConfig=MatchConfig
		self.Strategy=Strategy
		self.EventEngine=EventEngine
	# 处理账户下单
	def DealOrder(self,Code,Direction,Price,Volume,Account,Config):
		TempIndex,TempOrderNum,ret,RetValue=self.CheckOrder(Code,Direction,Price,Volume,Account,Config)
		self.MatchOrder(TempIndex,TempOrderNum,ret,RetValue)
		# if ret==ORDER_STATE.WAIT_TO_MATCH.value:
		# 	# 验单通过，开始撮合
		# 	MatchingRet,MatchingRetValue=self.MatchingSimulation(RetValue,TrdConfig={})
		# 	# 撮合结束，开始清算
		# 	# if MatchingRet!=ORDER_STATE.NOT_MATCHED.value:
		# 	Log.info([MatchingRet,MatchingRetValue])
		# 	self.DealMatchedRet2(TempIndex,TempOrderNum,MatchingRet,MatchingRetValue)
		# elif ret==ORDER_STATE.ORDER_CANCEL.value:
		# 	# 验单不通过，删除订单，加入订单记录
		# 	self.OrderRec[TempIndex][TempOrderNum]=self.Order[TempIndex][TempOrderNum].copy()
		# 	self.OrderRec[TempIndex][TempOrderNum]['Config']['OrderCancelReson']=RetValue
		# 	self.OrderRec[TempIndex][TempOrderNum]['State']=ret
		# 	self.Order[TempIndex]=self.Order[TempIndex].drop(TempOrderNum,1)
	def MatchOrder(self,TempIndex,TempOrderNum,ret,RetValue):
		if ret==ORDER_STATE.WAIT_TO_MATCH.value:
			# 验单通过，开始撮合
			MatchingRet,MatchingRetValue=self.MatchingSimulation(RetValue,TrdConfig={})
			# 撮合结束，开始清算
			# if MatchingRet!=ORDER_STATE.NOT_MATCHED.value:
			Log.info([MatchingRet,MatchingRetValue])
			self.DealMatchedRet2(TempIndex,TempOrderNum,MatchingRet,MatchingRetValue)
		elif ret==ORDER_STATE.ORDER_CANCEL.value:
			# 验单不通过，删除订单，加入订单记录
			self.OrderRec[TempIndex][TempOrderNum]=self.Order[TempIndex][TempOrderNum].copy()
			self.OrderRec[TempIndex][TempOrderNum]['Config']['OrderCancelReson']=RetValue
			self.OrderRec[TempIndex][TempOrderNum]['State']=ret
			self.Order[TempIndex]=self.Order[TempIndex].drop(TempOrderNum,1)
	# 撮合结果清算
	def DealMatchedRet(self,TempIndex,TempOrderNum,ret,RetValue):
		Code=self.Order[TempIndex][TempOrderNum]['Code']
		Direction=self.Order[TempIndex][TempOrderNum]['Direction']
		Price=self.Order[TempIndex][TempOrderNum]['Price']
		Volume=self.Order[TempIndex][TempOrderNum]['Volume']
		Account=self.Order[TempIndex][TempOrderNum]['Account']
		Config=self.Order[TempIndex][TempOrderNum]['Config']
		# 根据撮合结果更新信息
		if ret==ORDER_STATE.ALL_MATCHED.value:
			# 如果撮合成功
			Log.info('[OrderMatched]%s,%s,%s,%s,%s,%s' %(Code,Direction,RetValue[0],RetValue[1],RetValue[2],ret))
			# 更新订单记录情况
			self.OrderRec[TempIndex][TempOrderNum]=[Code,Direction,Price,Volume,0,ORDER_STATE.NOT_MATCHED.value,0,self.Time,TempOrderNum,'Mkt',self,{}]
			self.OrderRec[TempIndex][TempOrderNum]['State']=ret # OrderRec记录状态
			self.OrderRec[TempIndex][TempOrderNum]['AvgMatchingPrice']=RetValue[0] # OrderRec记录状态
			self.OrderRec[TempIndex][TempOrderNum]['VolumeMatched']=self.OrderRec[TempIndex][TempOrderNum]['VolumeMatched']+RetValue[1]
			# 更新订单情况
			if Direction==DIRECTION.LONG_BUY.value:
				CashFrozen=self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']
			self.Order[TempIndex]=self.Order[TempIndex].drop(TempOrderNum,1)# del self.Order[TempIndex][TempOrderNum] # Order中去除记录，也可用OrderList=OrderList.drop[TempOrderNum]
			if Code in self.Position[TempIndex].columns:# 如果持仓已经有相应Code了
				if Direction==DIRECTION.LONG_BUY.value:
					# # 更新持仓，先更新平均成本，后更新量
					self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*self.Position[TempIndex][Code]['Vol']+RetValue[2])/(self.Position[TempIndex][Code]['Vol']+RetValue[1])
					self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']+RetValue[1]
					# PriceNow不应该等于撮合价格，因为撮合价格是考虑了滑点的存在，而是应该等于QuotationNow中的价格
					# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
					self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
					self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
					# 更新AccountConfig
					self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-CashFrozen
					self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+CashFrozen-RetValue[2]
					self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']-RetValue[2]
					# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					# 这里要考虑不用list插值的方式，容易出错
					TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
					self.DealRec[TempIndex][TempDealRecNum]=self.OrderRec[TempIndex][TempOrderNum].copy()
					self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
					self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
					self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
					self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平仓盈亏（适用于全平）

				elif Direction==DIRECTION.LONG_SELL.value:
					# 判断是不是全部平仓
					if self.Position[TempIndex][Code]['Vol']-RetValue[1]!=0:
						# 更新持仓,先更新平均持仓成本
						self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*self.Position[TempIndex][Code]['Vol']-RetValue[2])/(self.Position[TempIndex][Code]['Vol']-RetValue[1])
						# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
						self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
						self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']-RetValue[1]
						self.Position[TempIndex][Code]['VolFrozen']=self.Position[TempIndex][Code]['VolFrozen']-RetValue[1]
						# self.Position[TempIndex][Code]['VolA']：可用量这里不变，因为订单来的时候已经扣除了
						self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
						self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
						self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
						CloseProfit=0
					else:
						CloseProfit=(RetValue[0]-self.Position[TempIndex][Code]['AvgCost'])*RetValue[1]
						self.Position[TempIndex]=self.Position[TempIndex].drop(Code,1)
					# 更新AccountConfig
					self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+RetValue[2]
					self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']+RetValue[2]
					# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					# 这里要考虑不用list插值的方式，容易出错
					TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
					self.DealRec[TempIndex][TempDealRecNum]=self.OrderRec[TempIndex][TempOrderNum].copy()
					self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
					self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
					self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=CloseProfit # 平仓盈亏（适用于全平）
					self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平均撮合价格

			else:# 如果持仓不含相应Code,则肯定是开仓
				# 更新持仓
				self.Position[TempIndex][Code]=[Code,0,0,0,0,0,'PriceNow',0,0,0,CURRENCY.CNY.value,'Mkt',self.Account[TempIndex],{}]
				self.Position[TempIndex][Code]['AvgCost']=RetValue[2]/RetValue[1]
				self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']+RetValue[1]
				# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
				self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
				self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
				self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
				self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
				# 更新AccountConfig
				self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-CashFrozen
				self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+CashFrozen-RetValue[2]
				self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']-RetValue[2]
				# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
				self.DealRec[TempIndex][TempDealRecNum]=self.OrderRec[TempIndex][TempOrderNum].copy()
				self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
				self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
				self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
				self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平均撮合价格（适用于全平）
			CloseProfit=self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']
			Log.info('[DealRec]%s,%s,%s,%s,%s,%s,%s' %(Code,Direction,RetValue[0],RetValue[1],RetValue[2],ret,CloseProfit))

		elif ret==ORDER_STATE.PART_MATCHED.value:
			Log.info('[OrderMatched]%s,%s,%s,%s,%s,%s' %(Code,Direction,RetValue[0],RetValue[1],RetValue[2],ret))
			# 更新订单情况
			self.Order[TempIndex][TempOrderNum]['State']=ret # Order记录状态
			self.Order[TempIndex][TempOrderNum]['AvgMatchingPrice']=RetValue[0] # OrderRec记录状态
			self.Order[TempIndex][TempOrderNum]['VolumeMatched']=self.Order[TempIndex][TempOrderNum]['VolumeMatched']+RetValue[1]
			if Direction==DIRECTION.LONG_BUY.value:
				CashFrozen=(self.Order[TempIndex][TempOrderNum]['VolumeMatched'])*self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']/self.Order[TempIndex][TempOrderNum]['Volume']
				self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']=self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']-CashFrozen
			if Code in self.Position[TempIndex].columns:# 如果持仓已经有相应Code了
				if Direction==DIRECTION.LONG_BUY.value:
					# # 更新持仓，先更新平均成本，后更新量
					self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*self.Position[TempIndex][Code]['Vol']+RetValue[2])/(self.Position[TempIndex][Code]['Vol']+RetValue[1])
					self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']+RetValue[1]
					# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
					self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
					self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
					# 更新AccountConfig
					self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-CashFrozen
					self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+CashFrozen-RetValue[2]
					self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']-RetValue[2]
					# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					# 这里要考虑不用list插值的方式，容易出错
					TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
					self.DealRec[TempIndex][TempDealRecNum]=self.Order[TempIndex][TempOrderNum].copy()
					# for TempField in self.Order[TempIndex][TempOrderNum].index:
					# 	self.DealRec[TempIndex][TempDealRecNum][TempField]=self.Order[TempIndex][TempOrderNum][TempField]
						# pass
					self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
					self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
					self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
					self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平仓盈亏（适用于全平）

				elif Direction==DIRECTION.LONG_SELL.value:
					# 更新持仓,先更新平均持仓成本
					if self.Position[TempIndex][Code]['Vol']-RetValue[1]!=0:
						self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*self.Position[TempIndex][Code]['Vol']-RetValue[2])/(self.Position[TempIndex][Code]['Vol'-RetValue[1]])
					else:
						self.Position[TempIndex][Code]['AvgCost']=0
					# self.Position[TempIndex][Code]['VolA']=self.Position[TempIndex][Code]['VolA']-RetValue[1]
					self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']-RetValue[1]
					self.Position[TempIndex][Code]['VolFrozen']=self.Position[TempIndex][Code]['VolFrozen']-RetValue[1]
					# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
					self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
					self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
					self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
					# 更新AccountConfig
					self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+RetValue[2]
					self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']+RetValue[2]
					# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					# 这里要考虑不用list插值的方式，容易出错
					TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
					self.DealRec[TempIndex][TempDealRecNum]=self.Order[TempIndex][TempOrderNum].copy()
					# for TempField in self.Order[TempIndex][TempOrderNum].index:
					# 	self.DealRec[TempIndex][TempDealRecNum][TempField]=self.Order[TempIndex][TempOrderNum][TempField]
					self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
					self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
					self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
					self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平仓盈亏（适用于全平）

			else:# 如果持仓不含相应Code,则肯定是开仓
				# 更新持仓
				self.Position[TempIndex][Code]=[Code,0,0,0,0,RetValue[2]/RetValue[1],'PriceNow',0,0,0,CURRENCY.CNY.value,'Mkt',self.Account[TempIndex],{}]
				self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']+RetValue[1]
				# self.Position[TempIndex][Code]['PriceNow']=RetValue[0]
				self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
				self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
				self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol']
				self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost']
				# 更新订单
				if Direction==1:
					CashFrozen=(self.Order[TempIndex][TempOrderNum]['VolumeMatched'])*self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']/self.Order[TempIndex][TempOrderNum]['Volume']
					self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']=self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']-CashFrozen
				# 更新AccountConfig
				self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-CashFrozen
				self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+CashFrozen-RetValue[2]
				self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']-RetValue[2]
				# 更新成交记录+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				# 这里要考虑不用list插值的方式，容易出错
				TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
				self.DealRec[TempIndex][TempDealRecNum]=self.Order[TempIndex][TempOrderNum].copy()
				# for TempField in self.Order[TempIndex][TempOrderNum].index:
				# 	self.DealRec[TempIndex][TempDealRecNum][TempField]=self.Order[TempIndex][TempOrderNum][TempField]
				self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
				self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 成交量（适用于部分成交）
				self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
				self.DealRec[TempIndex][TempDealRecNum]['AvgMatchingPrice']=RetValue[0] # 平仓盈亏（适用于全平）

			# 这里还是不要写成事件引擎的方式，因为异步处理在时间上很麻烦，遂直接调用；
			Event_OrderReturn=EventMod.Event(EventMod.EVENT_ORDERRETURN)
			# self.EventEngine.AddEvent(Event_OrderReturn)
			self.Account[TempIndex].Refresh(Event_OrderReturn)
		elif ret==ORDER_STATE.NOT_MATCHED.value:
			# 订单未匹配，需要做的有：
			# 1.记录当前订单在self.Order中；
			# 2.输出未匹配日志
			Log.info('[OrderMatched]%s,%s,%s' %(Code,ret,RetValue))

		elif ret==ORDER_STATE.ORDER_CANCEL.value:
			Log.info('[OrderMatched]%s,%s,%s' %(Code,ret,RetValue))
			# 订单无效，主要是金额和可用量不够
			# 更新订单记录情况
			self.OrderRec[TempIndex][TempOrderNum]=[Code,Direction,Price,Volume,0,ORDER_STATE.NOT_MATCHED.value,0,self.Time,TempOrderNum,'Mkt',self,{}]
			self.OrderRec[TempIndex][TempOrderNum]['State']=ret # OrderRec记录状态
			self.OrderRec[TempIndex][TempOrderNum]['Config']['OrderCancelReson']=RetValue
			# 需要移除订单，同时OrderRec记录这笔订单
			self.Order[TempIndex]=self.Order[TempIndex].drop(TempOrderNum,1)# del self.Order[TempIndex][TempOrderNum] # Order中去除记录，也可用OrderList=OrderList.drop[TempOrderNum]

		# 添加回执结果事件
		# 这里还是不要写成事件引擎的方式，因为异步处理在时间上很麻烦，遂直接调用；
		Event_OrderReturn=EventMod.Event(EventMod.EVENT_ORDERRETURN)
		# self.EventEngine.AddEvent(Event_OrderReturn)
		self.Account[TempIndex].Refresh(Event_OrderReturn)
	def DealMatchedRet2(self,TempIndex,TempOrderNum,ret,RetValue):
		# 判断撮合是否发生了成交
		if ret==ORDER_STATE.NOT_MATCHED.value:
			# 只用及记录OrderRec即可
			self.OrderRec[TempIndex][TempOrderNum]=self.Order[TempIndex][TempOrderNum]
			return
		# 现在知道模拟撮合结果和对应订单
		# 需要调整Position，DealRec，Order和OrderRec
		Code=self.Order[TempIndex][TempOrderNum]['Code']
		Direction=self.Order[TempIndex][TempOrderNum]['Direction']
		Price=self.Order[TempIndex][TempOrderNum]['Price']
		Volume=self.Order[TempIndex][TempOrderNum]['Volume']
		Account=self.Order[TempIndex][TempOrderNum]['Account']
		Config=self.Order[TempIndex][TempOrderNum]['Config']
		# 1、持仓Position清算
		# 判断有无持仓，没有则新建持仓
		if Code not in self.Position[TempIndex].columns:
			# self.Position[TempIndex][Code]=POSITION_INDEX
			self.Position[TempIndex][Code]=[Code,0,0,0,0,0,0,0,0,0,CURRENCY.CNY.value,'Mkt',self.Account[TempIndex],{}]
		# 计算持仓字段
		LastVol=self.Position[TempIndex][Code]['Vol']
		self.Position[TempIndex][Code]['Code']=Code
		if Direction==DIRECTION.LONG_BUY.value:
			self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']+RetValue[1]
			self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*LastVol+RetValue[2])/(LastVol+RetValue[1])
		elif Direction==DIRECTION.LONG_SELL.value:
			self.Position[TempIndex][Code]['Vol']=self.Position[TempIndex][Code]['Vol']-RetValue[1]
			self.Position[TempIndex][Code]['VolFrozen']=self.Position[TempIndex][Code]['VolFrozen']-RetValue[1]
			if (LastVol-RetValue[1])!=0:
				self.Position[TempIndex][Code]['AvgCost']=(self.Position[TempIndex][Code]['AvgCost']*LastVol-RetValue[2])/(LastVol-RetValue[1])
			else:
				self.Position[TempIndex][Code]['AvgCost']=0
		self.Position[TempIndex][Code]['PriceNow']=self.QuotationsNow[Code]['CP']
		self.Position[TempIndex][Code]['MktValue']=self.Position[TempIndex][Code]['PriceNow']*self.Position[TempIndex][Code]['Vol']
		self.Position[TempIndex][Code]['FloatingProfit']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])*self.Position[TempIndex][Code]['Vol'] if self.Position[TempIndex][Code]['AvgCost']!=0 else 0
		self.Position[TempIndex][Code]['ProfitRatio']=(self.Position[TempIndex][Code]['PriceNow']-self.Position[TempIndex][Code]['AvgCost'])/self.Position[TempIndex][Code]['AvgCost'] if self.Position[TempIndex][Code]['AvgCost']!=0 else 0
		# 2、订单Order清算
		# 计算Order字段
		LastVolumeMatched=self.Order[TempIndex][TempOrderNum]['VolumeMatched']
		# Code,Direction,Volumn,Price是第一次发送订单的时候就生成的，不能改变
		self.Order[TempIndex][TempOrderNum]['VolumeMatched']=self.Order[TempIndex][TempOrderNum]['VolumeMatched']+RetValue[1]
		self.Order[TempIndex][TempOrderNum]['State']=ret
		self.Order[TempIndex][TempOrderNum]['AvgMatchingPrice']=(self.Order[TempIndex][TempOrderNum]['AvgMatchingPrice']*LastVolumeMatched+RetValue[2])/(LastVolumeMatched+RetValue[1])
		# self.Order[TempIndex][TempOrderNum]['OrderTime']=self.Order[TempIndex][TempOrderNum]['OrderTime']
		LastCashFrozen=self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']
		self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']=self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']*(1-RetValue[1]/Volume)
		# 3、资金AccountConfig清算
		if Direction==DIRECTION.LONG_BUY.value:
			self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']-RetValue[2]
			self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-LastCashFrozen+self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']
			self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['Cash']-self.AccountConfig[TempIndex]['CashFrozen']
		elif Direction==DIRECTION.LONG_SELL.value:
			self.AccountConfig[TempIndex]['Cash']=self.AccountConfig[TempIndex]['Cash']+RetValue[2]
			self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+RetValue[2]
		# 4、成交记录DealRec清算
		# 增加一条成交记录
		TempDealRecNum=self.DealRec[TempIndex].shape[1]+1
		self.DealRec[TempIndex][TempDealRecNum]=self.Order[TempIndex][TempOrderNum].copy()
		# 计算DealRec字段
		self.DealRec[TempIndex][TempDealRecNum]['MatchingTime']=self.Time # 成交时间
		# 'Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice'已经在Order中算过了
		self.DealRec[TempIndex][TempDealRecNum]['MatchingVol']=RetValue[1] # 本次成交量
		self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=0 # 平仓盈亏（适用于全平）
		# 5、订单记录OrderRec清算
		# 保持和对应Order一致即可
		self.OrderRec[TempIndex][TempOrderNum]=self.Order[TempIndex][TempOrderNum]

		# 6、逐记录清算完毕，开始判断订单是否全部成交，仓位是否平光了
		if ret==ORDER_STATE.ALL_MATCHED.value:
			# 订单全部成交了
			# 订单冻结资金如果还有剩下的，加回CashA,修改OrderRec
			self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']
			self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']-self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']
			self.OrderRec[TempIndex][TempOrderNum]['Config']['CashFrozen']=0
			# 删除订单
			self.Order[TempIndex]=self.Order[TempIndex].drop(TempOrderNum,1)
		if self.Position[TempIndex][Code]['Vol']==0:
			# 计算平仓盈亏
			self.DealRec[TempIndex][TempDealRecNum]['CloseProfit']=(RetValue[0]-self.Position[TempIndex][Code]['AvgCost'])*RetValue[1]
			# 仓位全部平掉了
			# 删除持仓记录
			self.Position[TempIndex]=self.Position[TempIndex].drop(Code,1)

	# 验单进行资金冻结等
	# 主要内容：1.判断价格是否正确（涨跌停以内）;2.判断可用资金和可用量是否充足。
	def CheckOrder(self,Code,Direction,Price,Volume,Account,Config):
		# 识别相应账户在MatchingSys中的位置
		TempIndex=self.Account.index(Account)
		# 订单来了，先记录这笔订单
		self.OrderNum=self.OrderNum+1
		TempOrderNum=self.OrderNum
		# 处理持仓订单
		self.Order[TempIndex][TempOrderNum]=[Code,Direction,Price,Volume,0,ORDER_STATE.NOT_MATCHED.value,0,self.Time,TempOrderNum,'Mkt',self.Account[TempIndex],{'CashFrozen':0}]
		if Code in self.Position[TempIndex].columns:
			Position=self.Position[TempIndex]
		else:
			Position=pd.DataFrame(index=POSITION_INDEX)
			Position[Code]=[Code,0,0,0,0,0,'PriceNow',0,0,0,CURRENCY.CNY.value,'Mkt',self.Account[TempIndex],{'CashFrozen':0}]
		# 这里先生成TempOrder，避免后面的Price变化计算的冻结资金会会影响到原始订单的撮合
		RetValue={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'Account':Account,'Config':{}}
		# 判断是否在涨跌停价格以内
		if Price!=0 and (Price>self.QuotationsNow[Code]['Price_LimitUp'] or Price<self.QuotationsNow[Code]['Price_LimitDown']):
			Log.info('订单价格不在有效范围内，订单无效')
			ret=ORDER_STATE.ORDER_CANCEL.value
			RetValue=ORDER_CANCEL_REASON.WRONG_ORDER_PRICE.value
			return TempIndex,TempOrderNum,ret,RetValue
		# 其他判断
		if Direction==1:
			CostRatio=self.MatchConfig['CostRatio']
			# 判断是不是市价下单,是的话，价格按涨停价格下单冻结资金
			if Price==0:
				Price=self.QuotationsNow[Code]['Price_LimitUp']
			if Volume*Price*(1+CostRatio)>self.AccountConfig[TempIndex]['CashAvailable']:
				Log.info('可用资金不足，订单无效')
				ret=ORDER_STATE.ORDER_CANCEL.value
				RetValue=ORDER_CANCEL_REASON.CASH_AVAILABLE_NOT_ENOUGH.value
				return TempIndex,TempOrderNum,ret,RetValue
			else:
				# 可用资金足够，冻结部分,这里还要考虑是不是市价下单，我觉得是不是市价单可以在前面转化订单的时候转化成以张跌停价下单。
				self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']-Volume*Price*(1+CostRatio)
				self.AccountConfig[TempIndex]['CashFrozen']=self.AccountConfig[TempIndex]['CashFrozen']+Volume*Price*(1+CostRatio)
				self.Order[TempIndex][TempOrderNum]['Config']['CashFrozen']=Volume*Price*(1+CostRatio) # 订单记录中添加一个该订单冻结资金值
				ret=ORDER_STATE.WAIT_TO_MATCH.value
				# ret,RetValue=self.MatchingSimulation(TempOrder,TrdConfig={})
		elif Direction==0:
			if Price==0:
				Price=self.QuotationsNow[Code]['Price_LimitDown']
			if Volume>Position[Code]['VolA']:
				Log.info ("可用持仓不足，订单无效")
				ret=ORDER_STATE.ORDER_CANCEL.value
				RetValue=ORDER_CANCEL_REASON.VOL_AVAILABLE_NOT_ENOUGH.value
				return TempIndex,TempOrderNum,ret,RetValue
			else:
				# 可用持仓足够，冻结部分
				Position[Code]['VolA']=Position[Code]['VolA']-Volume
				Position[Code]['VolFrozen']=Position[Code]['VolFrozen']+Volume
				ret=ORDER_STATE.WAIT_TO_MATCH.value
		return TempIndex,TempOrderNum,ret,RetValue
	# 撮合
	def MatchingSimulation(self,Order,TrdConfig):
		# 最新修改的，撮合之前已经把资金和可用持仓判断过了
		Price4Trd=self.QuotationsNow[Order['Code']]['CP']
		Volume4Trd=self.QuotationsNow[Order['Code']]['VOL']
		Slippage=self.MatchConfig['Slippage']
		MarketPartcipation=self.MatchConfig['MarketPartcipation']
		CostRatio=self.MatchConfig['CostRatio']
		# d.成交价格比对
		# d.1 获取对应标的数据
		# TempVolA=Position[TempUnderLying]['VolA']
		Volume4Trd=Volume4Trd*MarketPartcipation
		# d.2 进行比对
		# d.2.1 市价开多仓
		if Order['Price']==0 and Order['Direction']==DIRECTION.LONG_BUY.value:
			PriceMatched=Price4Trd+Slippage
		# d.2.3 限价开多仓
		elif (Order['Price']>=Price4Trd) and Order['Direction']==DIRECTION.LONG_BUY.value:
			PriceMatched=Price4Trd
		# d.2.5 市价平多仓
		elif Order['Price']==0 and Order['Direction']==DIRECTION.LONG_SELL.value:
			PriceMatched=Price4Trd-Slippage
		# d.2.7 限价平多仓
		elif Order['Price']<Price4Trd and Order['Direction']==DIRECTION.LONG_SELL.value:
			PriceMatched=Price4Trd
		else:
			return ORDER_STATE.NOT_MATCHED.value,ORDER_CANCEL_REASON.PRICE_NOT_MATCHED.value
		# e.成交量比对
		# e.2 进行对比
		# 计算受市场参与度影响下的整数的市场成交量
		TempVolume4Trd=math.floor(Volume4Trd/100)*100
		if TempVolume4Trd==0:
			VolumeMatched=0
			# 当前没有成交量
			return ORDER_STATE.NOT_MATCHED.value,ORDER_CANCEL_REASON.NO_VOL_FOR_TRADING_NOW.value
		elif Order['Volume']<=TempVolume4Trd:
			VolumeMatched=Order['Volume']
			# 全部成交
			ret=ORDER_STATE.ALL_MATCHED.value
		elif Order['Volume']>TempVolume4Trd:
			VolumeMatched=TempVolume4Trd
			# 部分成交
			ret=ORDER_STATE.PART_MATCHED.value
		# f.资金情况的对比
		# f.1 开仓考虑资金情况
		if Order['Direction']==DIRECTION.LONG_BUY.value:
			CashMatched=PriceMatched*VolumeMatched*(1+CostRatio)
		# 平仓计算收入
		else:
			CashMatched=PriceMatched*VolumeMatched*(1-CostRatio)
		# 对当前标的的回测成交量进行扣除
		self.QuotationsNow[Order['Code']]['VOL']=self.QuotationsNow[Order['Code']]['VOL']-VolumeMatched
		return ret,[PriceMatched,VolumeMatched,CashMatched]
	def RefreshQoutation(self,Event_DataFeed):
		# 来行情了先记录之前的资金状态
		for TempIndex in range(0,self.Account.__len__()):
			TempSecurityValue=self.Position[TempIndex].loc['MktValue'].sum()
			TempCashRec=[self.Time.strftime("%Y-%m-%d %H:%M:%S.000"),\
						 TempSecurityValue+self.AccountConfig[TempIndex]['Cash'],self.AccountConfig[TempIndex]['Cash'], \
						 self.AccountConfig[TempIndex]['CashAvailable'],self.AccountConfig[TempIndex]['CashFrozen'],\
						 self.AccountConfig[TempIndex]['InitCash'],TempSecurityValue]
			self.CashRec[TempIndex]=pd.concat([self.CashRec[TempIndex],pd.DataFrame(TempCashRec,index=CASH_REC_INDEX)],axis=1)
		self.QuotationsNow=Event_DataFeed.Value['Data'].loc[self.QuotationsNow.index] # 这里只要用于撮合的字段就够了，不需要全部的订阅字段
		TempTime=datetime.strptime(Event_DataFeed.Value['Date'],'%Y-%m-%d %H:%M:%S.000')
		# 这是整个事件驱动引擎的最后一步，需要在这里判断回测是不是结束了------------
		TempEndTime=datetime.strptime(self.MatchConfig['EndTime'],'%Y-%m-%d %H:%M:%S')
		if TempEndTime==TempTime:
			self.IsRunning=False
		#------------------------------------------------------------------------
		if TempTime.date()!=self.Time.date():
			# 如果前后日期不相等，刷新可用持仓量，委托单等
			# 逐账户撤掉所有的委托单
			for TempIndex in range(0,len(self.Order)):
				# 把订单冻结资金加回可用资金
				self.AccountConfig[TempIndex]['CashAvailable']=self.AccountConfig[TempIndex]['CashAvailable']+self.AccountConfig[TempIndex]['CashFrozen']
				self.AccountConfig[TempIndex]['CashFrozen']=0
				# 将订单加入订单记录
				for TempColumn in self.Order[TempIndex].columns:
					# 更改Order状态等
					self.Order[TempIndex][TempColumn]['Config']['CancelReason']=ORDER_CANCEL_REASON.AUTO_CANCEL_EVERYDA.value
					self.Order[TempIndex][TempColumn]['State']=ORDER_STATE.ORDER_CANCEL.value
					# 更新订单记录
					# self.OrderRec[TempIndex]=pd.concat([self.OrderRec[TempIndex],self.Order[TempIndex]],axis=1)
					self.OrderRec[TempIndex][TempColumn]=self.Order[TempIndex][TempColumn]
				# 清除所有订单
				self.Order[TempIndex]=pd.DataFrame(index=ORDER_INDEX)
			# 考虑下单冻结量
			# map(lambda x:x.loc['VolA']=x.loc['Vol']-x.loc['VolFrozen'],self.Position)
			for TempPosition in self.Position:
				# TempPosition.loc['VolA']=TempPosition.loc['Vol']-TempPosition.loc['VolFrozen']
				TempPosition.loc['VolA']=TempPosition.loc['Vol']
				TempPosition.loc['VolFrozen']=0
		Log.info('RefreshQoutation Success!')
		self.Time=TempTime
		self.DealRemainOrder()
		# 通知Account刷新持仓数据，这里不能用事件的方式通知，因为可能并不及时
		map(lambda x:x.Refresh(EventMod.Event(EventMod.EVENT_ORDERRETURN)),self.Strategy.Account)
	def DealRemainOrder(self):
		# 新行情来了，原来没撮合的订单开始撮合，由于现在数据都是接的日频数据，跨日订单都被清理掉了，这部分没法测试，之后研究下分时的行情驱动
		# 先注释掉
		# 1.先验单，不同于CheckOrder
		# 2.MatchOrder就好了
		for TempIndex in range(0,len(self.Order)):
			for TempOrderNum in self.Order[TempIndex].columns:
				Code=self.Order[TempIndex][TempOrderNum]['Code']
				Direction=self.Order[TempIndex][TempOrderNum]['Direction']
				Price=self.Order[TempIndex][TempOrderNum]['Price']
				Volume=self.Order[TempIndex][TempOrderNum]['Volume']
				Account=self.Order[TempIndex][TempOrderNum]['Account']
				RetValue={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'Account':Account,'Config':{}}
				ret=ORDER_STATE.WAIT_TO_MATCH.value
				self.MatchOrder(TempIndex,TempOrderNum,ret,RetValue)
	def PerformanceStatistics(self):
		# 新建回测结果文件夹
		Temp_BackTestResult_Path=self.Strategy.Path+"\\"+self.Strategy.Name+"_BackTestResult"
		if not os.path.exists(Temp_BackTestResult_Path):
			os.makedirs(Temp_BackTestResult_Path)
		Temp_BackTestResult_Path=Temp_BackTestResult_Path+"\\"+datetime.now().strftime("%Y%m%d%H%M%S")
		os.makedirs(Temp_BackTestResult_Path)
		# 保存回测结果
		for TempAccountIndex in range(0,self.Account.__len__()):
			self.Order[TempAccountIndex].T.to_csv(Temp_BackTestResult_Path+"\\"+str(TempAccountIndex)+"_Order.csv")
			self.OrderRec[TempAccountIndex].T.to_csv(Temp_BackTestResult_Path+"\\"+str(TempAccountIndex)+"_OrderRec.csv")
			self.DealRec[TempAccountIndex].T.to_csv(Temp_BackTestResult_Path+"\\"+str(TempAccountIndex)+"_DealRec.csv")
			self.Position[TempAccountIndex].T.to_csv(Temp_BackTestResult_Path+"\\"+str(TempAccountIndex)+"_Position.csv")
			self.CashRec[TempAccountIndex].T.to_csv(Temp_BackTestResult_Path+"\\"+str(TempAccountIndex)+"_CashRec.csv")


class DataFeed(object):
	# 这里就是模拟行情推送的地方
	def __init__(self,MatchingSys):
		self.StartTime=MatchingSys.MatchConfig['StartTime']
		self.EndTime=MatchingSys.MatchConfig['EndTime']
		self.DataPar=MatchingSys.MatchConfig['DataPar']
		# 频率的配置应该是从策略订阅的频率中来的
		self.DataPar['TimeInterval']=MatchingSys.Strategy.QuoteDataConfig['TimeInterval']
		self.CodeList=MatchingSys.Strategy.QuoteDataConfig['CodeList']
		# Fields部分应该去取的是订阅数据和撮合数据的并集---------------------------------------------------------
		self.Fields=list(set(MatchingSys.MatchConfig['Fields']).union(set(MatchingSys.Strategy.QuoteDataConfig['Item'])))
		self.MatchingSys=MatchingSys  # 好像用不到MatchingSys，之后考虑删不删除
	def Run(self):
		# a.提取数据：目前考虑的是先全部提取，然后循环推送，以后数据量大了可能会考虑分段提取推送
		Data,ItemList,TimeList=PushMod.GetData(self.Fields, self.StartTime, self.EndTime, self.CodeList, self.DataPar)
		##################分割线##########################
		# 回测这里，本来需要按代码，按列表推，因为考虑到市面上的接口基本是采用回调的方式来订阅行情的
		# 但是在实际策略中，需要用于决策的往往是代码数据表的形式，在我们策略接口处的可定也是多代码组合，这里需要想一下
		# 目前的话还是先采用代码表的形式推送，后期可能根据不同的策略订阅的类型，采用不同的推送方式，留坑待补
		##################分割线##########################
		#代码进行到这，其实已经把所有的数据都提出来
		for tempdate in TimeList:
		# 到这，可以按日期推送数据了，在推送之前，需要把这些数据按策略整合成表的形式，推送给不同的策略；
			DataFeedEvent=EventMod.Event(EventMod.EVENT_DATAFEED)
			DataFeedEvent.Value['Date']=tempdate
			DataFeedEvent.Value['CodeList']=self.MatchingSys.Strategy.QuoteDataConfig['CodeList']
			# DataFeedEvent.Value['Item']=self.MatchingSys.Strategy.QuoteDataConfig['Item']
			DataFeedEvent.Value['Item']=ItemList
			# DataFeedEvent.Value['Strategy']=self.MatchingSys.Strategy
			DataFeedEvent.Value['Data']=pd.DataFrame(columns=DataFeedEvent.Value['CodeList'],index=DataFeedEvent.Value['Item'])
			for tempitem in ItemList:
				# DataFeedEvent.Value['Data'].loc[tempitem]=Data[ItemList.index(tempitem)].Value.ix[tempdate,DataFeedEvent.Value['CodeList']]
				DataFeedEvent.Value['Data'].loc[tempitem]=list(Data[tempitem].ix[tempdate])
			self.MatchingSys.EventEngine.AddEvent(DataFeedEvent)


## 回测模块函数
if __name__=='__main__':
	pass
	# test
	#
