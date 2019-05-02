# -*- coding: utf-8 -*-
import uuid
import DataServer.QOperation as Q

NAMESPACE_ACCOUNTID=uuid.UUID('be2257f6-6c2e-11e9-94e1-08606e0f5471') #用于生成AccountID的命名空间

BUFFSIZE=1024 #接收消息缓存区大小，如果以后传的消息多了会修改


# Position：证券代码，持仓量，可用量，冻结量，股票实际，成本价，市价，市值，浮动盈亏，盈亏比例，币种，交易市场，账户
POSITION_INDEX=['AccountID','Code','Vol','VolA','VolF','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','AddPar']
# Order：证券代码，方向，委托价格，委托数量，成交数量，备注（成交状态），成交均价，委托时间，订单编号，交易市场，账户
ORDER_INDEX=['AccountID','OrderID','Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','Mkt','AddPar']
# 资金表
CASHINFO_INDEX=["AccountID","Cash","CashA","CashF","InitCash"]
CASHFDETIAL_INDEX=['ID','Reason','Amt','Body','Fee']
ACCOUNTPAR_DAFAULT={'CommissionRate':0,'Slippage':0}

# 初始化KDB操作对象
DataOperationObject = Q.Q(**{"host": 'localhost', "port": 9568, "numpy_temporals": True})
DataOperationObject.AddTable("Client_Order", {
	"OrderID": "guid",
	"Code": "symbol",
	"Direction": "int",
	"Price": "float",
	"Volume": "int",
	"VolumeMatched": "int",
	"State": "symbol",
	"AvgMatchingPrice": "float",
	"OrderTime": "datetime",
	"Mkt": "symbol",
	"AccountID": "guid",
	"AddPar": "json"
}, ColList=ORDER_INDEX)
DataOperationObject.AddTable("Client_OrderRec", {
	"OrderID": "guid",
	"Code": "symbol",
	"Direction": "int",
	"Price": "float",
	"Volume": "int",
	"VolumeMatched": "int",
	"State": "symbol",
	"AvgMatchingPrice": "float",
	"OrderTime": "datetime",
	"Mkt": "symbol",
	"AccountID": "guid",
	"AddPar": "json"
}, ColList=ORDER_INDEX)
DataOperationObject.AddTable("Client_Position", {
	"AccountID":"guid",
	"Code":"symbol",
	"Vol":"int",
	"VolA":"int",
	"VolF":"int",
	"StockActualVol":"int",
	"AvgCost":"float",
	"PriceNow":"float",
	"MktValue":"float",
	"FloatingProfit":"float",
	"ProfitRatio":"float",
	"Currency":"symbol",
	"Mkt":"symbol",
	"AddPar":"json"
}, ColList=POSITION_INDEX)
DataOperationObject.AddTable("Client_CashInfo", {
	"AccountID":"guid",
	"Cash": "float",
	"InitCash": "float",
	"CashA": "float",
	"CashF": "float"
}, ColList=CASHINFO_INDEX)
DataOperationObject.AddTable("Exchange_OrderPool", {
	"AccountID": "guid",
	"OrderID": "guid",
	"Code": "symbol",
	"Direction": "int",
	"Price": "float",
	"Volume": "int",
	"VolumeMatched": "int",
	"State": "symbol",
	"AvgMatchingPrice": "float",
	"OrderTime": "datetime",
	"Mkt": "symbol",
	"AddPar": "json"
}, ColList=ORDER_INDEX)
DataOperationObject.AddTable("Exchange_ConnectInfo", {
	"ClientID": "guid",
	"Usr": "symbol",
	"AccountID": "guid",
	"ConnectState": "int",
	"Addr": "symbol",
	"ConnectTime": "datetime"
}, ColList=["ClientID", "Usr", "AccountID", "ConnectState", "Addr", "ConnectTime"])
