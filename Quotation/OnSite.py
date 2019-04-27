# -*- coding: UTF-8 -*-

__author__="WindSing"

import os,sys
sys.path.append('.\\lib')
import time
import datetime
import numpy as np
from QtAPI import *
from QtDataAPI import *
import CallBack

# 写文件
def WriteFile(AimStr,FilePath,Mod='w',encoding='utf-8'):
	TempFile=open(FilePath,Mod,encoding=encoding)
	TempFile.write(AimStr)
	TempFile.close()
# 弹窗警告
def MsgBox(Str,Title="警告",FilePath="OnSite_Inspection.log"):
	print(Str,Title)
	try:
		ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S '
		localTime = time.strftime(ISOTIMEFORMAT, time.localtime())
		TempStr=str(localTime)+":"+Title+Str+"\n"
		WriteFile(TempStr,FilePath,'a+')
	except:
		print("弹出MsgBox失败！")
# 处理巡检项目结果
def DealRet(Item,ret=0,errMsg="",dataCols=[]):
	if ret == 0:
		if len(dataCols)!=0:
			print("[i] ",Item," Success! Rows = ", len(dataCols))
		else:
			print("[i] ",Item," Success!")
		pass
	else:
		MsgBox("[x] "+Item+"("+str(hex(ret))+"): ", errMsg)
# ---------------------------------------------------------------------------------------------------------
# 巡检项目
# 1.登录
def OSI_Login():
	ret, errMsg = QtLogin("nblfm_qt", "199568")
	# ret, errMsg = QtLogin("kfzh_qt", "J3D47RQT")  # 千惠资本
	# ret, errMsg = QtLogin("jbhb_qtapi", "7SZ8BV43")
	# ret, errMsg = QtLogin("lfm_qt", "Z3SBE6WK")
	# ret, errMsg = QtLogin("lfm_Test", "HEH38VGC")
	DealRet("QtLogin",ret,errMsg)
# 2.GetExchanges取交易所信息
def OSI_GetExchanges():
	ret, errMsg, dataCols = GetExchanges()
	DealRet("GetExchanges",ret,errMsg,dataCols)
	dataCols.to_csv('GetExchanges.csv')
# 3.GetTradeTypes取交易品种信息
def OSI_GetTradeTypes():
	securityType = "S0107"	#商品期货
	ret, errMsg, dataCols = GetTradeTypes(securityType, ['*'], "2017-06-16")
	DealRet("GetTradeTypes",ret,errMsg,dataCols)
	dataCols.to_csv('GetTradeTypes.csv')
# 4.GetTradeCalendar取交易日历
def OSI_GetTradeCalendar():
	markets = ["SSE"]
	ret, errMsg, dataCols = GetTradeCalendar(markets, "2016-9-1", "2016-9-18", ["*"])
	DealRet("GetTradeCalendar",ret,errMsg,dataCols)
	dataCols.to_csv('GetTradeCalendar.csv')
# 5.GetSnapData取行情快照
def OSI_GetSnapData():
	securities = ["000001.SZSE", "000002.SZSE", "600000.SSE", "600028.SSE"]
	fields = ["Symbol", "Market", "ShortName", "TradingTime", "OP", "S1", "SV1", "B1", "BV1"]
	fields=['*']
	ret, errMsg, dataCols = GetSnapData(securities, [], EQuoteData["k_L2Transaction"], fields)
	DealRet("GetSnapData",ret,errMsg,dataCols)
	dataCols.to_csv('GetSnapData.csv')
# 6.GetPlates取所有板块信息
def OSI_GetPlates():
	securityType = ["S0101"]    #股票
	plateTypes = ["P4906"]	    #证监会行业类板块
	ret, errMsg, dataCols = GetPlates(False, securityType, plateTypes)
	DealRet("GetPlates",ret,errMsg,dataCols)
	dataCols.to_csv('GetPlates.csv')
# 7.GetRelatedPlates取证券归属的所有板块信息
def OSI_GetRelatedPlates():
	securities = ["000001.SZSE"]
	ret, errMsg, dataCols = GetRelatedPlates(securities)
	DealRet("GetRelatedPlates",ret,errMsg,dataCols)
	dataCols.to_csv('GetRelatedPlates.csv')
# 8.GetPlateSymbols取板块包含的证券清单信息(只支持查询叶子节点)
def OSI_GetPlateSymbols():
	plateIDs = [1301001]
	# plateIDs = [1701]
	ret,errMsg,dataCols = GetPlateSymbols(plateIDs, ESetOper["k_SetUnion"],[ESortType['k_SortDesc']],dateBegin='2017-04-01',dateEnd='2017-04-01')
	dataCols.to_csv("PlateConcept.csv")
	DealRet("GetPlateSymbols",ret,errMsg)
	dataCols.to_csv('GetPlateSymbols.csv')
# 9.GetSecurityInfo取提取股票、基金、债券、期货、个股期权、股指期权、指数的静态信息
def OSI_GetSecurityInfo():
	securities = ["A1509.DCE","000001.SZSE"]
	securities = ["1301021.*"]
	fields = ["Symbol","Market", "ShortName"]
	ret, errMsg, dataCols = GetSecurityInfo(securities, [], fields)
	dataCols.to_csv("PlateConcept.csv")
	DealRet("GetSecurityInfo",ret,errMsg,dataCols)
	dataCols.to_csv('GetSecurityInfo.csv')
# 10.GetSecurityCurInfo取提取股票、基金、债券、期货、个股期权、股指期权、指数的盘前信息
def OSI_GetSecurityCurInfo():
	securities = ["000001.SZSE", "000002.SZSE", "600000.SSE", "600028.SSE"]
	securities = ["1012003002017.*"]
	# securities = ["10001057.SSE", "10001058.SSE", "10001116.SSE"]
	fields = ["Symbol","Market", "ShortName", "TotalShare", "LCP", \
				  "LimitUp", "LimitDown", "NAPS", "EPS"]
	fields = ["ShortName",'PYShortName',"Symbol"]
	ret, errMsg, dataCols = GetSecurityCurInfo(securities, [], fields)
	dataCols.to_csv("PlateConcept.csv")
	DealRet("GetSecurityCurInfo",ret,errMsg,dataCols)
	dataCols.to_csv('GetSecurityCurInfo.csv')
# 11.GetDataByTime按时间取历史数据，默认数据先按日期和时间排序，再按证券代码排序
def OSI_GetDataByTime():
	securities=["000099.SZSE","000100.SZSE","000150.SZSE","000151.SZSE","000153.SZSE","000155.SZSE","000156.SZSE","000157.SZSE","000158.SZSE","000159.SZSE"]
	# securities=["1001001.*"]
	# fields=["TradingDate","TradingTime","Symbol"] #,"Market","OP","HIP","LOP","CP","CQ","CM","Position"]
	fields=['*']
	timePeriods = [['2019-01-09 15:00:00.000', '2019-01-10 15:00:00.000']]
	ret, errMsg, dataCols = GetDataByTime(securities, [], fields, \
											EQuoteType["k_Minute"], 1, timePeriods)	
	dataCols.to_csv('TrdMin.txt')
	DealRet("GetDataByTime",ret,errMsg,dataCols)
	dataCols.to_csv('GetDataByTime.csv')
# 12.GetDataByCount按数量取历史数据，默认数据先按日期和时间排序，
def OSI_GetDataByCount():
	securities = ["000001.SZSE", "000002.SZSE", "600000.SSE", "600028.SSE"]
	fields = ["Symbol","Market", "TradingTime", "OP", "HIP", "LOP", "CP"]
	ret, errMsg, dataCols = GetDataByCount(securities, [], fields, EQuoteType["k_Minute"],\
									 5, "2017-06-04 00:00:00.000", EDirection["k_Forward"], 100)
	DealRet("GetDataByCount",ret,errMsg,dataCols)
	dataCols.to_csv('GetDataByCount.csv')
# 13.GetTickByTime按时间取TICK数据
def OSI_GetTickByTime():
	security = " ZC1906.CZCE"
	security = " CF1901.CZCE"
	# fields = ["TradingDate","Symbol","Market", "TradingTime", "OP", "HIP", "LOP", "CP","TQ","TT","TM"]
	fields = ["TradingDate","Symbol","Market", "TradingTime", "BUYLEVELNO","SELLLEVELNO"]
	timePeriods = [['2018-12-13 17:00:00.000', '2018-12-14 17:00:00.000']]
	ret, errMsg, dataCols = GetTickByTime(security, 0, fields, timePeriods)
	DealRet("GetTickByTime",ret,errMsg,dataCols)
	dataCols.to_csv('GetTickByTime.csv')
	dataCols.to_csv("AimData.csv")
# 14.GetTickByCount按数量取TICK数据
def OSI_GetTickByCount():
	security = "SR1809-P-7400.CZCE"
	fields = ["Symbol","ShortName", "TradingTime", "OP", "HIP", "LOP", "CP"]
	ret, errMsg, dataCols = GetTickByCount(security, 0, ['*'],\
									"2017-05-04 00:00:00.000", EDirection["k_Forward"], 100)
	DealRet("GetTickByCount",ret,errMsg,dataCols)
	dataCols.to_csv('GetTickByCount.csv')
# 15.GetL2TickByTime按时间取Level-2数据（支持沪深股票）
def OSI_GetL2TickByTime():
	# security = "000001.SZSE"
	security = "000909.SZSE"
	fields = ["TradingTime"]
	timePeriods = [['2019-01-11 9:30:00.000', '2019-01-11 15:30:00.000']]
	ret, errMsg, dataCols = GetL2TickByTime(security, 0, EQuoteData["k_L2Quote"],\
										  fields, timePeriods)

	dataCols.to_csv('AimData.txt')
	DealRet("GetL2TickByTime",ret,errMsg,dataCols)
	dataCols.to_csv('GetL2TickByTime.csv')
# 16.GetL2TickByCount按数量取Level-2数据（支持沪深股票）
def OSI_GetL2TickByCount():
	security = "000001.SZSE"
	fields = ["Symbol","Market", "TradingTime", "OP", "HIP", "LOP", "CP"]
	ret, errMsg, dataCols = GetL2TickByCount(security, 0, EQuoteData["k_L2Quote"], fields, \
								"2017-06-04 00:00:00.000", EDirection["k_Forward"], 100)
	DealRet("GetL2TickByCount",ret,errMsg,dataCols)
	dataCols.to_csv('GetL2TickByCount.csv')
# 17.GetFinance取财务因子
def OSI_GetFinance():
	securities = ["000001.SZSE", "000002.SZSE", "600000.SSE", "600028.SSE"]
	fields = ["Symbol","Market", "BEPS", "TOTOR", "TOLPRO"]
	ret, errMsg, dataCols = GetFinance(securities, [], fields, "2017-01-01", "2017-04-01",\
							EReportType["k_RptMergeCur"], ETrailType["k_TrailSeason"], \
							ERptDateType["k_RptDateIssue"])
	DealRet("GetFinance",ret,errMsg,dataCols)
	dataCols.to_csv('GetFinance.csv')
# 18.GetFactor取量化及风控因子
def OSI_GetFactor():
	securities = ["000001.SZSE", "000002.SZSE", "600000.SSE", "600028.SSE"]
	fields = ["Symbol","Market", "TradingDate", "QF_NetAssetPS", "QF_PE"]
	ret, errMsg, dataCols = GetFactor(securities, [], fields, "2017-01-01", "2017-05-05")
	DealRet("GetFactor",ret,errMsg,dataCols)
	dataCols.to_csv('GetFactor.csv')
# 19.GetHisMarketInfo取证券历史变动信息（分红派息停复牌等）
def OSI_GetHisMarketInfo():
	securities = ["000552.SZSE"]#,"002226.SZSE"]#, "000552.SZSE", "600000.SSE", "600028.SSE"]
	fields = ["Symbol","Market", "CumulateBwardFactor1","TradingDate"]#,"ExDividendDate", "DividentBT", "BonusRatio"]
	ret,errMsg,dataCols = GetHisMarketInfo(securities, [], fields,\
												"2010-10-03", "2018-04-27")
	DealRet("GetHisMarketInfo",ret,errMsg,dataCols)
	dataCols.to_csv('GetHisMarketInfo.csv')
# 20.GetJointContracts取期货主力连续或连续合约信息，按连续合约代码和日期排序
def OSI_GetJointContracts():
	contracts = ["ACC01"]
	ret, errMsg, dataCols = GetJointContracts(contracts, "2013-11-29", "2017-07-29")
	DealRet("GetJointContracts",ret,errMsg,dataCols)
	dataCols.to_csv('GetJointContracts.csv')
	dataCols.to_csv("AimData.txt")
# 21.GetMonthBill查询月度数据计费清单
def OSI_GetMonthBill():
	ret, errMsg, dataCols = GetMonthBill( "2018-11-01", "2018-12-04")
	DealRet("GetMonthBill",ret,errMsg,dataCols)
	dataCols.to_csv('GetMonthBill.csv')
	dataCols.to_csv("千惠资本_MonthBill.csv")
# 22.GetDetailBill 查询数据计费明细
def OSI_GetDetailBill():
	ret, errMsg, dataCols = GetDetailBill("2018-11-01", "2018-12-04")
	DealRet("GetDetailBill",ret,errMsg,dataCols)
	dataCols.to_csv('GetDetailBill.csv')
	dataCols.to_csv("千惠资本_MDetailBill.csv")
# 23.QueryTable查询财经数据库单表
def OSI_QueryTable():
	tableName = 'BOND_BASICINFO';
	fields = ['BondID', 'FullName', 'UpdateID', 'UpdateTime'];
	conditions = [['BondID', EDataType['k_Double'], ECalcSign['k_GE'], ['10000']],\
					  ['BondID', EDataType['k_Double'], ECalcSign['k_LE'], ['11000']]];
	sorts = [['BONDID', ESortType["k_SortDesc"]]];
	page = [1, 100];
	ret, errMsg, dataCols = QueryTable(tableName, fields, conditions, sorts, page);
	DealRet("QueryTable",ret,errMsg,dataCols)
	dataCols.to_csv('QueryTable.csv')
# 24.轮询取当天股票Tick数据
def OSI_GetAllStockTickToday():
	securities = [1001001]
	TimeBegin=(datetime.datetime.now().date()-datetime.timedelta(1)).strftime('%Y-%m-%d 17:00:00')
	TimeEnd=(datetime.datetime.now().date()-datetime.timedelta(0)).strftime('%Y-%m-%d 17:00:00')
	ret, errMsg, dataCols = GetPlateSymbols(securities, ESetOper["k_SetUnion"],dateBegin=TimeBegin,dateEnd=TimeEnd)
	securities=list(dataCols['Symbol'].str.cat(dataCols['Market'],sep='.'))
	timePeriods=[[TimeBegin,TimeEnd]]
	TimeStart=datetime.datetime.now()
	fields=['*']
	n=0
	with open('Stock.txt','a') as f:
		f.write('\n'.join(securities))
	exit()
	with open('Record.txt','a') as f:
		for stock in securities:
			try:
				Begin=datetime.datetime.now()
				ret, errMsg, dataCols = GetL2TickByTime(stock, 0, EQuoteData["k_L2Quote"],\
												  fields, timePeriods)
				ret, errMsg, dataCols = GetL2TickByTime(stock, 0, EQuoteData["k_L2Quote"],\
												  fields, timePeriods)
				TimeDelta=str(datetime.datetime.now()-Begin)
				n=n+1
				record='%04d:%s:%s' %(n,str(stock),str(TimeDelta))
				print(record)
				f.write(record+'\n')
			except:
				pass
		f.write('Total:'+str(datetime.datetime.now()-TimeStart))
# 25.循环提取数据直到某一时间带点
def OSI_LoopByTime():
	TimeEnd=datetime.datetime(2018,12,18,21,12,0)
	print('开始查询！')
	while datetime.datetime.now()<TimeEnd:
		security = " CF1901.CZCE"
		fields = ["TradingDate","Symbol","Market", "TradingTime", "BUYLEVELNO","SELLLEVELNO"]
		timePeriods = [['2018-12-17 17:00:00.000', '2018-12-18 17:00:00.000']]
		ret, errMsg, dataCols = GetTickByTime(security, 0, fields, timePeriods)
		# if ('CZCE' in list(dataCols["Market"])) or (0 in list(dataCols["SELLLEVELNO"])):
		if (0 in list(dataCols["BUYLEVELNO"])) or (0 in list(dataCols["SELLLEVELNO"])):
			print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
			dataCols.to_csv(datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".csv")
		time.sleep(30)
# 26.当日板块代码循环提数
def OSI_LoopByPlate():
	securities = [1001001]
	TimeBegin=(datetime.datetime.now().date()-datetime.timedelta(1)).strftime('%Y-%m-%d 17:00:00')
	TimeEnd=(datetime.datetime.now().date()-datetime.timedelta(0)).strftime('%Y-%m-%d 17:00:00')
	ret, errMsg, dataCols = GetPlateSymbols(securities, ESetOper["k_SetUnion"],dateBegin=TimeBegin,dateEnd=TimeEnd)
	securities=list(dataCols['Symbol'].str.cat(dataCols['Market'],sep='.'))
	timePeriods=[[TimeBegin,TimeEnd]]
	fields=['*']
	# 自定义代码
	timePeriods=[['2019-01-10 17:00:00.000','2019-01-11 17:00:00.000']]
	fields=['TradingTime']
	securities=['000909.SZSE','002590.SZSE','300111.SZSE','300209.SZSE','300304.SZSE','300719.SZSE','300720.SZSE','300721.SZSE','300722.SZSE','300723.SZSE','300724.SZSE','300725.SZSE','300726.SZSE','300727.SZSE','300729.SZSE','300730.SZSE','300731.SZSE','300732.SZSE','300733.SZSE','300735.SZSE','300736.SZSE','300737.SZSE','300738.SZSE','300739.SZSE','300740.SZSE','300757.SZSE','601975.SSE','603121.SSE']
	# 自定义代码
	n=0
	with open('AimData.txt','a') as f:
		for stock in securities:
			try:
				# ret, errMsg, dataCols = GetDataByTime(securities, [], fields, EQuoteType["k_Minute"], 1, timePeriods)	
				ret, errMsg, dataCols = GetL2TickByTime(stock, 0, EQuoteData["k_L2Quote"],fields, timePeriods)
				n=n+1
				TempData=str(len(dataCols))
				print('{}| {}；'.format(stock,TempData))
				f.write(TempData+'\n')
			except:
				pass

# 25.QtLogOut从认证服务登出
def OSI_Logout(qt_usr="nblfm_qt"):
	ret, errMsg = QtLogout(qt_usr)
	DealRet("QtLogout",ret,errMsg)
# A.订阅k_Sts
def OSI_Sub_k_Sts():
	RegSubStsCB(CallBackFunc.OnSubSts)
	securities = ["1001001.*"]
	# securities = ['2101001001002.*']
	ret, errMsg = Subscribe(EQuoteData["k_Sts"], 60, securities, [])
	DealRet("Sub_k_Sts",ret,errMsg)
	# time.sleep(100000)
	# ret, errMsg = UnSubscribe(EQuoteData["k_Sts"], 60, securities, [])
	# DealRet("UnSub_k_Sts",ret,errMsg)
# B.订阅k_Sts
def OSI_Sub_k_StsPerTick():
	RegSubStsPerTickCB(CallBackFunc.OnSubSts)
	# securities = ["*.SSE"]
	securities = ['1001001.*']
	ret, errMsg = Subscribe(EQuoteData["k_StsPerTick"], 60, securities, [])
	DealRet("Sub_k_StsPerTick",ret,errMsg)
	time.sleep(100000)
	# ret, errMsg = UnSubscribe(EQuoteData["k_StsPerTick"], 60, securities, [])
	# DealRet("UnSub_k_StsPerTick",ret,errMsg)
# C.订阅L1_Quote
def OSI_Sub_L1_Quote():
	RegSubQuoteCB(CallBackFunc.OnSubQuote)
	securities = ["2101001001002.*"]
	ret, errMsg = Subscribe(EQuoteData["k_Quote"], 0, securities, [])
	DealRet("Sub_Quote",ret,errMsg)
	time.sleep(1000)
	ret, errMsg = UnSubscribe(EQuoteData["k_Quote"], 0, securities, [])
	DealRet("UnSub_Quote",ret,errMsg)
# D.订阅L2_Quote
def OSI_Sub_L2_Quote():
	RegSubL2QuoteCB(CallBackFunc.OnSubL2Quote)
	securities = ["10001544.SSE"]
	ret, errMsg = Subscribe(EQuoteData["k_L2Quote"], 0, securities, [])
	DealRet("Sub_L2_Quote",ret,errMsg)
	time.sleep(1000)
	ret, errMsg = UnSubscribe(EQuoteData["k_L2Quote"], 0, securities, [])
	DealRet("UnSub_L2_Quote",ret,errMsg)
# E.订阅L2Transaction
def OSI_Sub_L2_Transaction():
	RegSubL2TransactionCB(CallBackFunc.OnSubL2Transaction)
	securities = ['000001.SZSE','600000.SSE']
	ret, errMsg = Subscribe(EQuoteData["k_L2Transaction"], 0, securities, [])
	DealRet("Sub_L2_Transaction",ret,errMsg)
	time.sleep(1000)
	ret, errMsg = UnSubscribe(EQuoteData["k_L2Transaction"], 0, securities, [])
	DealRet("UnSub_L2_Transaction",ret,errMsg)
# F.订阅L2Transaction并计算延时
def OSI_Sub_L2_Transaction_DelayCalc():
	RegSubL2TransactionCB(CallBackFunc.OnSubL2Transaction_DelayCalc)
	securities = ['000001.SZSE','600000.SSE','000868.SZSE','300215.SZSE','002012.SZSE','002013.SZSE','002014.SZSE','002015.SZSE','002016.SZSE','002018.SZSE','300026.SZSE','000733.SZSE','601107.SSE','002020.SZSE','002021.SZSE','000665.SZSE','000667.SZSE','000668.SZSE','000670.SZSE','000672.SZSE','000928.SZSE','000929.SZSE','000802.SZSE','000803.SZSE','000807.SZSE','600600.SSE','001696.SZSE','000600.SZSE','000930.SZSE','000931.SZSE','000932.SZSE','002200.SZSE','002201.SZSE','002202.SZSE','000421.SZSE','000422.SZSE','000423.SZSE','000425.SZSE','000428.SZSE','000429.SZSE','000799.SZSE','000032.SZSE','000036.SZSE','000037.SZSE','000592.SZSE','000593.SZSE','000596.SZSE','000597.SZSE','000599.SZSE','002091.SZSE','002135.SZSE','300339.SZSE']
	securities=['300549.SZSE','000428.SZSE','300302.SZSE']
	ret, errMsg = Subscribe(EQuoteData["k_L2Transaction"], 0, securities, [])
	DealRet("Sub_L2_Transaction_DelayCalc",ret,errMsg)
	time.sleep(10000)
	ret, errMsg = UnSubscribe(EQuoteData["k_L2Transaction"], 0, securities, [])
	DealRet("UnSub_L2_Transaction_DelayCalc",ret,errMsg)
# Z.主程序
def Main():
	OSI_Login()
	# OSI_GetExchanges()
	# OSI_GetTradeTypes()
	# OSI_GetTradeCalendar()
	# OSI_GetSnapData()
	# OSI_GetPlates()
	# OSI_GetRelatedPlates()
	# OSI_GetPlateSymbols()
	# OSI_GetSecurityInfo()	
	# OSI_GetSecurityCurInfo()
	OSI_GetDataByTime()
	# OSI_GetDataByCount()
	# OSI_GetTickByTime()
	# OSI_GetTickByCount()
	# OSI_GetL2TickByTime()
	# OSI_GetL2TickByCount()
	# OSI_GetFinance()
	# OSI_GetFactor()
	# OSI_GetHisMarketInfo()
	# OSI_GetJointContracts()
	# OSI_GetMonthBill()
	# OSI_GetDetailBill()
	# OSI_QueryTable()
	# OSI_GetAllStockTickToday()
	# OSI_LoopByTime()
	# OSI_LoopByPlate()
	# OSI_Sub_k_Sts()
	# OSI_Sub_k_StsPerTick()
	# OSI_Sub_L1_Quote()
	# OSI_Sub_L2_Quote()
	# OSI_Sub_L2_Transaction()
	# OSI_Sub_L2_Transaction_DelayCalc()
	OSI_Logout()

if __name__=='__main__':
	Main()