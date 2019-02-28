# -*- coding: utf-8 -*-

import pandas as pd
import uuid
import datetime
import Common as cm

# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['Code','Vol','VolA','VolF','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','AddPar']
# 冻结资金明细
CASHFDETIAL_INDEX=['ID','Reason','Amt','Body','Fee']

ACCOUNTPAR_DAFAULT={'CommissionRate':0,'Slippage':0}

class Account(object):
	# 初始化,账户持仓信息中暂时没考虑多空双向持仓
	def __init__(self,Usr=None,Pwd=None,AddPar=None,Type='Stock',AccPar=ACCOUNTPAR_DAFAULT,MktSliNow=None,Exchange=None):
		self.Position=pd.DataFrame(index=POSITION_INDEX)
		self.Order=pd.DataFrame(index=ORDER_INDEX)
		self.OrderRec=pd.DataFrame(index=ORDER_INDEX)
		self.CashInfo={'Cash':0,'InitCash':0,'CashA':0,'CashF':0,'CashFDetial':pd.DataFrame(index=CASHFDETIAL_INDEX)}
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
		# Log.info('Refresh Position Success!')
		# 以下是测试用
		# if '000001.SZSE' in self.Position.columns:
			# Log.debug(list(self.Position['000001.SZSE']))

	# 获取持仓信息
	def GetPositionByCode(self,Code,Item=POSITION_INDEX):
		if type(Item) is not list:Item=[Item]
		if Code in self.Position.columns:
			return list(self.Position[Code].loc[Item])
		else:
			return [None]*len(Item)

	# 获取订单数据
	def GetOrderByID(self,OrderID,Item=ORDER_INDEX):
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
		# 订单数据
		Volume,VolumeMatched,State=self.GetOrderByID(OrderID,['Volume','VolumeMatched','State'])
		# 判断是否全部成交
		if Volume==VolumeMatched and State=='AllMatched':
			# 清除订单
			self.Order.drop(labels=OrderID,axis=1,inplace=True)
		return 1,''

	# 检查持仓数据（如无效持仓需要清理等）
	def CheckPositionByCode(self,Code):
		# 持仓数据
		Vol=self.GetPositionByCode(Code,'Vol')[0]
		# 判断是否全部成交
		if Vol==0:
			# 清除订单
			self.Position.drop(label=OrderID,axis=1,inplace=True)
		return 1,''

	# 根据成交回报处理OrderList
	def DealMatchRetInOrderList(self,OrderID,MatchInfo):
		# 订单数据
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
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
		# 回写数据到Order及OrderRec
		self.Order[OrderID]=[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config]
		self.OrderRec[OrderID]=[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config]
		# 检查订单状态（如订单全部成交则需要取消等）
		ret,msg=self.CheckOrderByID(OrderID)
		return 1,''

	# 根据成交回报处理PositionList
	def DealMatchRetInPositionList(self,OrderID,MatchInfo):
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,VolumeMatched_Order,State_Order,AvgMatchingPrice_Order,OrderTime_Order,OrderNum_Order,Mkt_Order,Account_Order,Config_Order=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		# 判断是否已有持仓
		if Code_Order in list(self.Position.columns):
			Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position=self.GetPositionByCode(Code_Order)
		else:
			Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position=[Code_Order,0,0,0,0,0,0,0,0,0,'CNY','Mkt',self,{}]
		# 初始化持仓字段
		Code,Vol,VolA,VolF,StockActualVol,AvgCost,PriceNow,MktValue,FloatingProfit,ProfitRatio,Currency,Mkt,Account,Config=Code_Position,Vol_Position,VolA_Position,VolF_Position,StockActualVol_Position,AvgCost_Position,PriceNow_Position,MktValue_Position,FloatingProfit_Position,ProfitRatio_Position,Currency_Position,Mkt_Position,Account_Position,Config_Position
		# 计算持仓字段
		# 主要分多空
		if Direction_Order==1:
			Vol=Vol_Position+VolumeMatching
			VolA=VolA_Position # 股票T+1，可用量不变
			VolF=VolF_Position
			StockActualVol=StockActualVol_Position
			AvgCost=(AvgCost_Position*Vol_Position+CashMatching)/Vol
		elif Direction_Order==0:
			Vol=Vol_Position-VolumeMatching
			VolA=VolA
			VolF=VolF_Position-VolumeMatching
			StockActualVol=StockActualVol_Position
			# 卖出平均成本=0 if 持仓=0 else （旧的平均成本*旧的持仓量-卖出收回资金）/新持仓量
			AvgCost=0 if Vol==0 else (AvgCost_Position*Vol_Position-CashMatching)/Vol
		# 回写数据到持仓数据中
		# 因为其他的字段都和实时行情有关，回写完毕后重新调用一个函数即可
		self.Position[Code]=[Code,Vol,VolA,VolF,StockActualVol,AvgCost,PriceNow,MktValue,FloatingProfit,ProfitRatio,Currency,Mkt,Account,Config]
		# 重新计算实时持仓盈亏
		ret,msg=self.CalcPositionRealTimeValueByCode(Code)
		# 检查持仓信息（如无效持仓清除等）
		ret,msg=self.CheckPositionByCode(Code)
		return 1,''

	# 更新资金信息CashInfo 
	def DealMatchRetInCashInfo(self,OrderID,MatchInfo):
		# 订单数据
		Code_Order,Direction_Order,Price_Order,Volume_Order,VolumeMatched_Order,State_Order,AvgMatchingPrice_Order,OrderTime_Order,OrderNum_Order,Mkt_Order,Account_Order,Config_Order=self.GetOrderByID(OrderID)
		# 成交数据
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# 柜台数据
		CommissionRate=self.AccPar['CommissionRate']
		# 成交金额计算
		CashMatching=PriceMatching*VolumeMatching*(1+CommissionRate) if Direction_Order==1 else PriceMatching*VolumeMatching*(1-CommissionRate)
		# 资金数据
		Cash_Old=self.CashInfo['Cash']
		InitCash_Old=self.CashInfo['InitCash']
		CashA_Old=self.CashInfo['CashA']
		CashF_Old=self.CashInfo['CashF']
		# 开始计算
		# 买入计算
		if Direction_Order==1:
			Cash=Cash_Old-CashMatching
			InitCash=InitCash_Old
			CashA=CashA_Old
			CashF=CashF_Old-CashMatching
		elif Direction_Order==0:
			Cash=Cash_Old+CashMatching
			InitCash=InitCash_Old
			CashA=CashA_Old+CashMatching
			CashF=CashF_Old
		# 回写数据
		self.CashInfo['Cash']=Cash
		self.CashInfo['InitCash']=InitCash
		self.CashInfo['CashA']=CashA
		self.CashInfo['CashF']=CashF
		return 1,''
		

	# 计算实时持仓价值
	def CalcPositionRealTimeValueByCode(self,Code):
		if Code not in self.Position.columns:return 0,'无效Code！'
		# 市场数据
		Price=self.MktSliNow.GetDataByCode(Code,'Price')
		# 更新数据
		self.Position[Code].loc['PriceNow']=Price
		self.Position[Code].loc['MktValue']=Price*self.Position[Code].loc['Vol']
		self.Position[Code].loc['FloatingProfit']=(Price-self.Position[Code].loc['AvgCost'])*self.Position[Code].loc['Vol']
		self.Position[Code].loc['ProfitRatio']=(Price-self.Position[Code].loc['AvgCost'])/self.Position[Code].loc['AvgCost'] if self.Position[Code].loc['AvgCost']!=0 else 0
		return 1,''
		
	# 出来订单成交回报
	def DealMatchRet(self,OrderID,MatchInfo,MatchTime):
		# 更新订单列表
		ret,msg=self.DealMatchRetInOrderList(OrderID,MatchInfo)
		# 更新持仓列表
		ret,msg=self.DealMatchRetInPositionList(OrderID,MatchInfo)
		# 更新资金列表
		ret,msg=self.DealMatchRetInCashInfo(OrderID,MatchInfo)
		return 1,''

	# 账户下单
	def PlaceOrder(self,Code,Direction,Price,Volume,AddPar=None):
		Order={'Code':Code,'Direction':Direction,'Price':Price,'Volume':Volume,'AddPar':AddPar}
		# 验单
		MktInfo={'Price_LimitUp':self.MktSliNow.GetDataByCode(Code,'Price_LimitUp'),'Price_LimitDown':self.MktSliNow.GetDataByCode(Code,'Price_LimitDown')}
		ret,msg=self.CheckNewOrder(Order,MktInfo)
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
			CommissionRate=self.AccPar['CommissionRate']
			# 判断是不是市价下单,是的话，价格按涨停价格下单冻结资金
			if Price==0:
				Price2Frozen=MktInfo['Price_LimitUp']
			else:
				Price2Frozen=Price
			if Volume*Price2Frozen*(1+CommissionRate)>self.CashInfo['CashA']:
				ret=0
				msg='可用资金不足，订单无效'
				return ret,msg
		elif Direction==0:
			if Volume>(self.GetPositionByCode(Code,'VolA')[0] if self.GetPositionByCode(Code,'VolA')[0]!=None else 0):
				ret=0
				msg='可用持仓不足，订单无效'
				return ret,msg
		return 1,'订单有效'

	# 冻结资金持仓等
	# 验单通过的订单进行冻结资金的操作
	# 这里没有数据锁，可能出现验单通过实际冻结的时候却不足的问题吗？
	def FrozenNewOrder(self,OrderID):
		Code,Volume,Direction=self.GetOrderByID(OrderID,['Code','Volume','Direction'])
		# 买入冻结资金
		if Direction==1:
			FeeCalc=self.CalcOrderFee(OrderID)
			CashFrozen=FeeCalc['CashBody']+FeeCalc['Fee']
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
		# 记录订单
		self.Order[OrderID]=[Code,Direction,Price,Volume,0,'WaitToMatch',0,self.CreateOrderTime(),OrderID,'Mkt',self,AddPar]
		self.OrderRec[OrderID]=[Code,Direction,Price,Volume,0,'WaitToMatch',0,self.CreateOrderTime(),OrderID,'Mkt',self,AddPar]
		return OrderID
	
	# 发送新订单到“虚拟交易所”进行撮合
	def SendNewOrderToMatch(self,OrderID):
		Order=list(self.Order[OrderID])
		ret,msg=self.Exchange.DealNewOrder(OrderID,Order)	
		return ret,msg

	# 计算订单手续费等
	def CalcOrderFee(self,OrderID,MatchInfo=None):
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
			Price2Calc=MatchInfo['PriceMatching']
			Volume2Calc=MatchInfo['VolumeMatching']
		elif Price_Order==0:
			Price2Calc=Price_LimitUp
			Volume2Calc=Volume_Order
		else:
			Price2Calc=Price_Order
			Volume2Calc=Volume_Order
		# 费用主体
		CashBody=Price2Calc*Volume2Calc
		# 佣金
		CommissionFee=5 if CashBody*CommissionRate<5 else CashBody*CommissionRate
		# 印花税费=卖出成交额*0.001
		StampFee=CashBody*0.001 if Direction_Order==0 else 0
		# 过户费，仅上海股票
		if cm.GetExchangeByCode(Code_Order)=='SHSE':
			TransferFee=1 if Volume2Match/1000<1 else Volume2Match/1000
		else:
			TransferFee=0
		# 所有费用
		Fee=CommissionFee+StampFee+TransferFee
		# 返回结果
		return {'CashBody':CashBody,'Fee':Fee,'CommissionFee':CommissionFee,'StampFee':StampFee,'TransferFee':TransferFee}

if __name__=='__main__':
	# 验单函数的测试
	import Exchange
	import Market
	Account=Account('usr','pwd','AddPar',MktSliNow=Market.MktSliNow())
	Account.AccPar['CommissionRate']=0.01
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
		ret,msg=Account.SendNewOrderToMatch(OrderID)
		print([ret,msg])
	# 合起来测试
	ret, msg,OrderID=Account.PlaceOrder(**Order)
	print([ret,msg])