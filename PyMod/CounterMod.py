#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'

import pandas as pd
import copy
import GeneralMod
from datetime import datetime

# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['Code','Vol','VolA','FrozenVol','StockActualVol','Avgcost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
Log=GeneralMod.Log()
class Account(object):
	# 初始化，ForBackTest用于区别是连接实盘账户还是只是回测用
	def __init__(self,Usr=None,Pwd=None,Config=None,Type='Stock'):
		self.Position=pd.DataFrame(index=POSITION_INDEX)
		self.Order=pd.DataFrame(index=ORDER_INDEX)
		self.AccountConfig={'Cash':0,'InitCash':0,'CashAvailable':0,'CashFrozen':0}
		self.Connect(Usr,Pwd,Config)
	# 实盘账户初始化之后会连接柜台，获取交易参数等
	def Connect(self,Usr,Pwd,Config):
		# 如果是回测
		if Usr is None:
			Log.info('连接回测模拟柜台成功！')
			self.CounterType='BackTestCounter'
			self.MatchingSys=None
		else:
			# 省略连接真实柜台的大代码
			Log.info('连接XX柜台成功！')
			self.CounterType='XXCounter'

	# 刷新账户信息
	def Refresh(self,Event_OrderReturn):
		# 更新持仓信息
		if self.CounterType=='BackTestCounter':
			TempIndex=self.MatchingSys.Account.index(self)
			self.Position=self.MatchingSys.Position[TempIndex]
			self.Order=self.MatchingSys.Order[TempIndex]
			self.AccountConfig=self.MatchingSys.AccountConfig[TempIndex]
		elif self.CounterType=='XXCounter':
			pass
		Log.info('Refresh Position Success!')
		# 以下是测试用
		if '000001.SZSE' in self.Position.columns:
			Log.debug(list(self.Position['000001.SZSE']))


	# 获取持仓信息
	def GetPosition(self,Code='All',Item='All'):
		# 获取持仓信息
		if Code=='All':
			Code=list(self.Position.columns)
		if Item=='All':
			Item=list(self.Position.index)
		# 判断Code是否存在并返回
		if not type(Code)==list:
			Code=[Code]
		TempPosition=copy.deepcopy(self.Position)
		for TempCode in Code:
			if TempCode not in TempPosition.columns:
				TempPosition[TempCode]=[TempCode,0,0,0,0,0,'PriceNow',0,0,0,'CNY','Mkt',self,{}]
		return TempPosition[Code].loc[Item]

	# 账户下单
	def PlaceOrder(self,Code,Direction,Price,Volume):
		# OrderTime=self.MatchingSys.Time
		Config={'OrderTime':'OrderTime','State':'State'}
		Log.info('%s,%s,%s,%s' %(Code,Direction,Price,Volume))
		# self.Order[self.Order.shape[1]+1]=[Code,Direction,Price,Volume,'State','AvgMatchingPrice',OrderTime,'OrderNum','Mkt',self,{}]


		if self.CounterType=='BackTestCounter':
			self.MatchingSys.DealOrder(Code,Direction,Price,Volume,self,Config)
		elif self.CounterType=='XXCounter':
			pass


if __name__=='__main__':
	a=Account()
	a.GetPosition('000001.SZSE')