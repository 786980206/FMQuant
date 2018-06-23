#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WindSing'
####################################### 一些说明 #######################################################################
# 1.先用下GetPlate这个接口
####################################### 导入模块 #######################################################################
import time
import DataDef
import DataModify
import sys,os
# 必须要加上这句，不知道为什么
sys.path.append(DataDef.ROOT_PATH+r"\DataMod\GetDataByGTA_QTApi")
# print(sys.path)
# GetDataByGTA_QTApi.
# from QtAPI import *
import QtPyAPI
from QtDataAPI import *
import datetime
import pandas as pd
work_path=os.getcwd()
script_path = os.path.realpath(__file__)
os.chdir(os.path.dirname(script_path))
ret = QtPyAPI.QtLogin(QtPyAPI.string(),"nblfm_qt", "199568","")
os.chdir(work_path)
####################################### 常量定义 #######################################################################
# 交易所代码映射
GTA_QTAPI_EXCHANGE_TRAN={DataDef.EXCHANGE.SHSE.value:'SSE',
						 DataDef.EXCHANGE.SZSE.value:'SZSE'
						 }
# STOCK_BASIC字段映射
GTA_QTAPI_STOCK_BASIC_TRAN_FIELDS={DataDef.FIELDS_STOCK_BASIC.Code.value:'Symbol',      # 代码
							DataDef.FIELDS_STOCK_BASIC.Name.value:'ShortName',      # 名称
							DataDef.FIELDS_STOCK_BASIC.Exchange.value:'Market',			#交易所
							DataDef.FIELDS_STOCK_BASIC.Plate_Industry.value:'IndustryCode',       # 细分行业:数据源自证监会行业分类2012版,具体对照参照Doc目录
							# DataDef.FIELDS_STOCK_BASIC.Plate_Area.value:'area',      # 地区
							# DataDef.FIELDS_STOCK_BASIC.PE.value:'pe',        # 市盈率
							DataDef.FIELDS_STOCK_BASIC.Shares_Tradable.value:'CirShare',         # 流通股本
							DataDef.FIELDS_STOCK_BASIC.Shares_Total.value:'TotalShare',         # 总股本(万)
							# DataDef.FIELDS_STOCK_BASIC.Assets_Total.value:'totalAssets',         # 总资产(万)
							# DataDef.FIELDS_STOCK_BASIC.Assets_Liquid.value:'liquidAssets',        # 流动资产
							# DataDef.FIELDS_STOCK_BASIC.Assets_Fixed.value:'fixedAssets',         # 固定资产
							# DataDef.FIELDS_STOCK_BASIC.Reserved.value:'reserved',       # 公积金
							# DataDef.FIELDS_STOCK_BASIC.Reserved_PerShare.value:'reservedPerShare',         # 每股公积金
							DataDef.FIELDS_STOCK_BASIC.EPS.value:'EPS',       # 每股收益
							DataDef.FIELDS_STOCK_BASIC.BVPS.value:'NAPS',      # 每股净资
							# DataDef.FIELDS_STOCK_BASIC.PB.value:'pb',        # 市净率
							DataDef.FIELDS_STOCK_BASIC.Time_toMarket.value:'ListedDate',        # 上市日期
							# QTAPI独有的部分字段
							DataDef.FIELDS_STOCK_BASIC.CP_Last.value:'LCP',
							DataDef.FIELDS_STOCK_BASIC.Price_LimitUp.value:'LimitUp',
							DataDef.FIELDS_STOCK_BASIC.Price_LimitDown.value:'LimitDown'

							}
# K_DAY字段映射
GTA_QTAPI_K_DAY_TRAN_FIELDS={DataDef.FIELDS_K_DAY.Code.value:'Symbol',
					  		DataDef.FIELDS_K_DAY.Name.value:'ShortName',
					  		# DataDef.FIELDS_K_DAY.Exchange.value:'Exchange', # 日线行情不支持Exchange
							DataDef.FIELDS_K_DAY.Time.value:'TradingDate',
						 	DataDef.FIELDS_K_DAY.OP.value:'OP',
					  		DataDef.FIELDS_K_DAY.HP.value:'HIP',
					  		DataDef.FIELDS_K_DAY.LP.value:'LOP',
					  		DataDef.FIELDS_K_DAY.CP.value:'CP',
					  		DataDef.FIELDS_K_DAY.VOL.value:'CQ',
					  		DataDef.FIELDS_K_DAY.Amount.value:'CM',
							DataDef.FIELDS_K_DAY.Price_LimitUp.value:'LIMITUP',
							DataDef.FIELDS_K_DAY.Price_LimitDown.value:'LIMITDOWN' # API这里取日线行情的时候这两个字段是全部大写的！
						 }
####################################### 函数定义 #######################################################################
# 取股票基本信息
def Get_STOCK_BASIC_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	# ret, errMsg = QtLogin("nblfm_qt", "199568")
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	# Fields先转化为QTAPI能识别的
	TempCodeList=[x for x in CodeList if x.Exchange in GTA_QTAPI_EXCHANGE_TRAN.keys()]
	TempCodeList=[x.Code+'.'+GTA_QTAPI_EXCHANGE_TRAN[x.Exchange] for x in TempCodeList]
	if "Code" not in Fields:Fields.append("Code")
	Fields=[x for x in Fields if x in GTA_QTAPI_STOCK_BASIC_TRAN_FIELDS.keys()]
	TempFields=[GTA_QTAPI_STOCK_BASIC_TRAN_FIELDS[x] for x in Fields]
	# 开始提数
	if "GTA_QTApi_PLATE_ID" in SpecialConfig.keys():
		TempPlate=[SpecialConfig["GTA_QTApi_PLATE_ID"]+".*"]
		Ret.Value,Ret.RetReason,RetValue=GetSecurityCurInfo(TempPlate,[], TempFields)
		if Ret.Value==0:Ret.Value=DataDef.STATUS.SUCCESS.value
	else:
		Ret.Value,Ret.RetReason,RetValue=GetSecurityCurInfo(TempCodeList,[], TempFields)
		if Ret.Value==0:Ret.Value=DataDef.STATUS.SUCCESS.value
	# 数据提取完毕，再取相应字段
	RetValue=RetValue[TempFields]
	RetValue.columns=Fields
	RetValue=RetValue.set_index('Code')
	RetValue.index.name='Code'
	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,datetime.datetime.now().date().isoformat(),DataDef.GROUP_BY_TYPE.TIME.value)
	return Ret,RetValue
# 取证券日线数据
def Get_K_DAY_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	# Fields先转化为QTAPI能识别的
	TempCodeList=[x for x in CodeList if x.Exchange in GTA_QTAPI_EXCHANGE_TRAN.keys()]
	TempCodeList=[x.Code+'.'+GTA_QTAPI_EXCHANGE_TRAN[x.Exchange] for x in TempCodeList]
	if "Code" not in Fields:Fields.append("Code")
	if "Time" not in Fields:Fields.append("Time")
	Fields=[x for x in Fields if x in GTA_QTAPI_K_DAY_TRAN_FIELDS.keys()]
	TempFields=[GTA_QTAPI_K_DAY_TRAN_FIELDS[x] for x in Fields]
	# TimeList转化为QTAPI能识别的
	TempTimeList=[[TimeList.StartStr,TimeList.EndStr]]
	# 开始提数
	if "GTA_QTApi_PLATE_ID" in SpecialConfig.keys():
		TempPlate=[SpecialConfig["GTA_QTApi_PLATE_ID"]+".*"]
		if "GTA_QTApi_PRICE_ADJUST" in SpecialConfig.keys():
			Ret.Value,Ret.RetReason,RetValue=GetDataByTime(TempPlate,[], TempFields,EQuoteType["k_Day"],1,TempTimeList,priceAdj=EPriceAdjust[SpecialConfig["GTA_QTApi_PRICE_ADJUST"]])
		else:
			Ret.Value,Ret.RetReason,RetValue=GetDataByTime(TempPlate,[], TempFields,EQuoteType["k_Day"],1,TempTimeList)
		if Ret.Value==0:Ret.Value=DataDef.STATUS.SUCCESS.value
	else:
		if "GTA_QTApi_PRICE_ADJUST" in SpecialConfig.keys():
			Ret.Value,Ret.RetReason,RetValue=GetDataByTime(TempCodeList,[], TempFields,EQuoteType["k_Day"],1,TempTimeList,priceAdj=EPriceAdjust[SpecialConfig["GTA_QTApi_PRICE_ADJUST"]])
		else:
			Ret.Value,Ret.RetReason,RetValue=GetDataByTime(TempCodeList,[], TempFields,EQuoteType["k_Day"],1,TempTimeList)
		if Ret.Value==0:Ret.Value=DataDef.STATUS.SUCCESS.value
	# 数据提取完毕，再取相应字段
	# RetValue=RetValue[TempFields]
	RetValue.columns=Fields
	RetValue=RetValue.set_index('Time')
	RetValue.index.name='Time'
	# 再把数据按代码分组
	TempRetValue=RetValue.groupby(by=["Code"])
	RetValue=[]
	TempIndex=[]
	for TempName,TempGroup in TempRetValue:
		TempGroup=TempGroup.drop("Code",axis=1)
		RetValue.append(TempGroup)
		# TempName=TempName+"."+TempGroup
		TempIndex.append(TempName)
	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,TempIndex,DataDef.GROUP_BY_TYPE.CODE.value)
	return Ret,RetValue

# 取全部字段的处理
def GetAllFields(DataType):
	if DataType==DataDef.DATA_TYPE.K_DAY.value:
		RetValue=list(GTA_QTAPI_K_DAY_TRAN_FIELDS.keys())
	elif DataType==DataDef.DATA_TYPE.STOCK_BASIC.value:
		RetValue=list(GTA_QTAPI_STOCK_BASIC_TRAN_FIELDS.keys())
	return RetValue

######################################## 主程序 ########################################################################
if __name__=='__main__':

	# 登录认证服务，初始化QtAPI运行环境
	# ret, errMsg = QtLogin("nblfm_qt", "199568")
	# Get_STOCK_BASIC_Data(["000001.SZSE"],[],['*'])
	# Get_STOCK_BASIC_Data(["000001.SZSE"],[],['Symbol','Market', 'ShortName'])
	A,B=Get_STOCK_BASIC_Data(DataModify.CodeListModify(["000001.SZSE"]),[],['Code','Exchange','Name','Plate_Industry','CP_Last'],{"GTA_QTApi_PLATE_ID":"1001001"})
	A,B=Get_STOCK_BASIC_Data(DataModify.CodeListModify(["000001.SZSE"]),[],list(GTA_QTAPI_STOCK_BASIC_TRAN_FIELDS.keys()),{"GTA_QTApi_PLATE_ID":"1001001"})
	time.sleep(1)
	pass

# endof __main__