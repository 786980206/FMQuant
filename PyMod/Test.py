# -*- coding: utf-8 -*-
# 测试脚本的编写

# Counter.py ====================================================
import Exchange
import Market
import Counter
# 设置涨跌停价格等市场信息
Mkt=Market.MktSliNow()
Account=Counter.Account('usr','pwd','AddPar',MktSliNow=Mkt)
def Init(Mkt,Account):
	Mkt.Data['Price_LimitUp']=15
	Mkt.Data['Price_LimitDown']=5
	Mkt.Data['Price']=10
	Mkt.Data['Volume4Trd']=200
	# 设置账户信息
	Account.Exchange=Exchange.Exchange(MktSliNow=Mkt)
	Account.AccPar['CostRatio']=0.01
	Account.AccPar['Slippage'] = 0.1
	Account.CashInfo={'Cash': 10000, 'CashF': 0, 'InitCash': 10000, 'CashA': 10000}
	Account.Position['000001.SZSE']=['000001.SZSE',1200,600,600,0,0,'PriceNow',0,0,0,'CNY','Mkt',Account,{}]
# 开始测试
Init(Mkt,Account)
# 1、价格无效
Order={'Code':'000001.SZSE','Direction':0,'Price':100,'Volume':200,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print([ret,msg])
# 2、订单数量无效
Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':20,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print([ret,msg])
# 3、可用资金补助
Order={'Code':'000001.SZSE','Direction':1,'Price':9,'Volume':2000000,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print([ret,msg])
# 4、可用持仓不足
Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':700,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print([ret,msg])
# 5、可用持仓不足
Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':700,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print([ret,msg])
# 6、买入全部成交
Init(Mkt,Account)
Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':1,'Price':11,'Volume':100,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print(list(Account.Position['000001.SZSE']))
# 7、买入部分成交
Init(Mkt,Account)
Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':1,'Price':11,'Volume':300,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print(list(Account.Position['000001.SZSE']))
print(list(Account.Order[OrderID]))
# 8、买入未成交
Init(Mkt,Account)
Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':1,'Price':9,'Volume':300,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
# print(list(Account.Position['000001.SZSE']))
print(list(Account.Order[OrderID]))
# 9、卖出全部成交
Init(Mkt,Account)
# Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':100,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print(list(Account.Position['000001.SZSE']))
# 10、卖出部分成交
Init(Mkt,Account)
# Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':0,'Price':9,'Volume':300,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print(list(Account.Position['000001.SZSE']))
print(list(Account.Order[OrderID]))
# 11、卖出未成交
Init(Mkt,Account)
# Account.Position.drop(labels='000001.SZSE',axis=1,inplace=True)
Order={'Code':'000001.SZSE','Direction':0,'Price':11,'Volume':300,'AddPar':{}}
ret,msg,OrderID=Account.PlaceOrder(**Order)
print(list(Account.Position['000001.SZSE']))
print(list(Account.Order[OrderID]))
