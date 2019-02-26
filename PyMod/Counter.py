# -*- coding: utf-8 -*-

import pandas as pd
import uuid
import datetime

# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['Code','Vol','VolA','VolF','StockActualVol','Avgcost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','AddPar']

ACCOUNTPAR_DAFAULT={'CostRatio':0,'Slippage':0}

class Account(object):
	# 初始化,账户持仓信息中暂时没考虑多空双向持仓
	def __init__(self,Usr=None,Pwd=None,AddPar=None,Type='Stock',AccPar=ACCOUNTPAR_DAFAULT,MktSliNow=None,Exchange=None):
		self.Position=pd.DataFrame(index=POSITION_INDEX)
		self.Order=pd.DataFrame(index=ORDER_INDEX)
		self.CashInfo={'Cash':0,'InitCash':0,'CashA':0,'CashF':0}
		self.AccPar=AccPar # 柜台账户参数数据，如账户手续费，保证金等数据
		self.MktSliNow=MktSliNow # 当前行情切片，作为一个外部数据源供柜台模块引用
		self.Exchange=Exchange # 交易所对象，用于柜台发送订单进行撮合等
		self.Connect(Usr,Pwd,AddPar)
	# 实盘账户初始化之后会连接柜台，获取交易参数等
	def Connect(self,Usr,Pwd,AddPar):
		# 如果是回测
		if Usr is None:
			self.CounterType='BackTestCounter'
		else:
			# 省略连接真实柜台的大代码
			# Log.info('连接XX柜台成功！')
			self.CounterType='XXCounter'

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
		Log.info('Refresh Position Success!')
		# 以下是测试用
		if '000001.SZSE' in self.Position.columns:
			Log.debug(list(self.Position['000001.SZSE']))

	# 获取持仓信息
	def GetPosition(self,Code,Item):
		# 获取持仓信息
		if Code not in self.Position.columns:
			return 0
		else:
			return self.Position[Code].loc[Item]

	# 生成订单下单时间
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# 账户下单
	def PlaceOrder(self,Code,Direction,Price,Volume,AddPar=None):
		Order={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'AddPar':AddPar}
		# 验单
		MktInfo={'Price_LimitUp':self.MktSliNow.GetDataByCode(Code,'Price_LimitUp'),'Price_LimitDown':self.MktSliNow.GetDataByCode(Code,'Price_LimitDown')}
		ret,msg=self.CheckNewOrder(Order,MktInfo)
		if ret==0:
			return ret,msg,''
		else:
			# 资金冻结
			ret,msg=self.FrozenNewOrder(Order)
			# 记录订单
			OrderID=self.LogNewOrder(Order)
			# 发送到交易所撮合
			ret,msg,RetValue=self.SendNewOrderToMatch(OrderID)
		return ret,msg,RetValue

	# 订单校验
	# 验单进行资金冻结等
	# 需求参数：账户信息，订单信息(其中账户信息，参照CTP，可以自己进行订单验证)，验单需要的其他信息，如涨跌停价格
	# 主要内容：1.判断价格是否正确（涨跌停以内）;2.判断可用资金和可用量是否充足。
	def CheckNewOrder(self,Order,MktInfo):
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
		# 判断订单数量是否被100整除
		if Volume % 100!=0 or Volume<=0 :
			ret=0
			msg='输入订单数量无效！'
			return ret,msg
		# 其他判断
		if Direction==1:
			CostRatio=self.AccPar['CostRatio']
			# 判断是不是市价下单,是的话，价格按涨停价格下单冻结资金
			if Price==0:
				Price2Frozen=MktInfo['Price_LimitUp']
			else:
				Price2Frozen=Price
			if Volume*Price2Frozen*(1+CostRatio)>self.CashInfo['CashA']:
				ret=0
				msg='可用资金不足，订单无效'
				return ret,msg
		elif Direction==0:
			if Volume>	self.GetPosition(Code,'VolA'):
				ret=0
				msg='可用持仓不足，订单无效'
				return ret,msg
		return 1,'订单有效'

	# 冻结资金持仓等
	# 验单通过的订单进行冻结资金的操作
	# 这里没有数据锁，可能出现验单通过实际冻结的时候却不足的问题吗？
	def FrozenNewOrder(self,Order):
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']	
		# 买入冻结资金
		if Direction==1:
			CostRatio=self.AccPar['CostRatio']
			# 判断是不是市价下单,是的话，价格按涨停价格下单冻结资金
			if Price==0:
				Price2Frozen=MktInfo['Price_LimitUp']
			else:
				Price2Frozen=Price
			CashFrozen=Volume*Price2Frozen*(1+CostRatio) # 冻结资金=数量*价格*（1+手续费）
			self.CashInfo['CashA']=self.CashInfo['CashA']-CashFrozen
			self.CashInfo['CashF']=self.CashInfo['CashF']+CashFrozen
		elif Direction==0:
			self.Position[Code].loc['VolA']=self.Position[Code].loc['VolA']-Volume
			self.Position[Code].loc['VolF']=self.Position[Code].loc['VolF']+Volume
		return 1,'冻结资金持仓成功！'

	# 记录新订单，将新订单加入订单记录中并生成订单id 
	def LogNewOrder(self,Order):
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# 生成订单编号
		OrderID=str(uuid.uuid1())
		self.Order[OrderID]=[Code,Direction,Price,Volume,0,'wait2match',0,self.CreateOrderTime(),OrderID,'Mkt',self,AddPar]
		return OrderID
	
	# 发送新订单到“虚拟交易所”进行撮合
	def SendNewOrderToMatch(self,OrderID):
		Order=list(self.Order[OrderID])
		ret,msg,RetValue=self.Exchange.DealNewOrder(OrderID,Order)	
		return ret,msg,RetValue

if __name__=='__main__':
	# 验单函数的测试
	import Exchange
	import Market
	Account=Account('usr','pwd','AddPar',MktSliNow=Market.MktSliNow())
	Account.AccPar['CostRatio']=0.01
	Account.AccPar['Slippage'] = 0.1
	Account.CashInfo={'Cash': 10000, 'CashF': 0, 'InitCash': 10000, 'CashA': 10000}
	Account.Position['000001.SZSE']=['000001.SZSE',1200,600,600,0,0,'PriceNow',0,0,0,'CNY','Mkt',Account,{}]
	Account.Exchange=Exchange.Exchange(MktSliNow=Market.MktSliNow())
	MktInfo={'Price_LimitUp':10.20,'Price_LimitDown':8.0}
	Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':200,'AddPar':{}}
	ret,msg=Account.CheckNewOrder(Order,MktInfo)
	print([ret,msg])
	# 冻结资金函数测试
	if ret==1:
		ret,msg=Account.FrozenNewOrder(Order)
		print(list(Account.Position['000001.SZSE']))
		print(Account.CashInfo)
		OrderID=Account.LogNewOrder(Order)
		print(list(Account.Order[OrderID]))
		# 撮合成交设置
		ret,msg,RetValue=Account.SendNewOrderToMatch(OrderID)
		print([ret,msg,RetValue])
	# 合起来测试
	ret, msg, RetValue=Account.PlaceOrder(**Order)
	print([ret,msg,RetValue])