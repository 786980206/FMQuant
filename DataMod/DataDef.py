#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'
####################################### 一些说明 #######################################################################
#

####################################### 导入模块 #######################################################################
import datetime
from dateutil import parser
import pandas as pd
from enum import Enum
####################################### 常量定义 #######################################################################
ROOT_PATH=r"E:\OneDrive\0_Coding\010_MyQuantSystem\Beta4.0"
# 交易所代码映射
TRAN_EXCHANGE={'SZ':'SZSE','SZSE':'SZSE','SH':'SHSE','SHSE':'SHSE','SSE':'SHSE'}
# 字段代码映射(用作把用户输入的字段映射成系统能识别的标准代码)
TEMP_TRAN_FIELDS={
				'Code':['CODE','SYMBOL'],
				'Name':['NAME','SHORTNAME'],
				'Exchange':['EXCHANGE','MARKET'],
				'Time':['TIME'],
				# K_DAY
				'CP':['CP','CLOSE','CLOSEPRICE','C'],
				'OP':['OP','OPEN','OPENPRICE','O'],
				'HP':['HP','HIGH','HIGHPRICE','H','HIP'],
				'LP':['LP','LOW','LOWPRICE','L','LOP'],
				'VOL':['VOL','VOLUME','V','CQ'],
				'Amount':['AMOUNT'],
				# STOCK_BASIC
				'Plate_Industry':['PLATE_INDUSTRY'],
				'Plate_Area':['PLATE_AREA'],
				'PE':['PE'],
				'Shares_Tradable':['SHARES_TRADABLE'],
				'Shares_Total':['SHARE_TOTAL'],
				'Assets_Total':['ASSETS_TOTAL'],
				'Assets_Liquid':['ASSETS_LIQUID'],
				'Assets_Fixed':['ASSETS_FIXED'],
				'Reserved':['RESERVED'],
				'Reserved_PerShare':['RESERVED_PERSHARE'],
				'EPS':['EPS'],
				'BVPS':['BVPS'],
				'PB':['PB'],
				'Time_toMarket':['TIME_TOMARKET'],
				'CP_Last':['CP_LAST'],	# 前收盘价
				'Price_LimitUp':['PRICE_LIMITUP','HARDENPRICE'],	# 涨停价
				'Price_LimitDown':['PRICE_LIMITDOWN','DROPSTOPPRICE']	# 跌停价
				  }
# 生成TRAN_FIELDS
def CreateReverseDict(DictGiven):
	RetValue={}
	for TempKeys,TempValue in DictGiven.items():
		for TempItem in TempValue:
			RetValue[TempItem]=TempKeys
	return RetValue
TRAN_FIELDS=CreateReverseDict(TEMP_TRAN_FIELDS)
####################################### 枚举类型定义 #######################################################################
# 所有的枚举类型都写在这里，因为这个文件会用作其他程序的配置文件
# EnumStart----------------------------------
# K_DAY字段枚举值
class FIELDS_K_DAY(Enum):
	Code='Code'      # 代码
	Name='Name'      # 名称
	Exchange='Exchange'      # 交易所
	Time='Time'
	OP='OP'
	HP='HP'
	CP='CP'
	LP='LP'
	VOL='VOL'
	Amount='Amount'
	Price_LimitUp='Price_LimitUp'
	Price_LimitDown='Price_LimitDown'
# K_DAY字段枚举值
class FIELDS_K_MIN(Enum):
	Code='Code'      # 代码
	Name='Name'      # 名称
	Exchange='Exchange'      # 交易所
	Date='Date'
	Time='Time'
	OP='OP'
	HP='HP'
	CP='CP'
	LP='LP'
	VOL='VOL'
	Amount='Amount'
# STOCK_BASIC字段枚举值
class FIELDS_STOCK_BASIC(Enum):
	# TuShare字段
	Code='Code'      # 代码
	Name='Name'      # 名称
	Exchange='Exchange'      # 交易所
	Plate_Industry='Plate_Industry'       # 细分行业
	Plate_Area='Plate_Area'      # 地区
	PE='PE'        # 市盈率
	Shares_Tradable='Shares_Tradable'         # 流通股本
	Shares_Total='Shares_Total'         # 总股本(万)
	Assets_Total='Assets_Total'         # 总资产(万)
	Assets_Liquid='Assets_Liquid'        # 流动资产
	Assets_Fixed='Assets_Fixed'         # 固定资产
	Reserved='Reserved'       # 公积金
	Reserved_PerShare='Reserved_PerShare'         # 每股公积金
	EPS='EPS'       # 每股收益,净利润
	BVPS='BVPS'      # 每股净资
	PB='PB'        # 市净率
	Time_toMarket='Time_toMarket'        # 上市日期
	# QTAPI部分字段
	CP_Last='CP_Last'	# 前收盘价
	Price_LimitUp='Price_LimitUp'	# 涨停价
	Price_LimitDown='Price_LimitDown'	# 跌停价
# 状态枚举
class STATUS(Enum):
	FAIL=0
	SUCCESS=1
# 时间枚举
class TIME_INTERVAL(Enum):
	UNK=0
	SEC_01=1
	MIN_01=60
	DAY_01=86400
# 数据类型枚举，因为不同的数据类型需要用到不同的Tushare接口
class DATA_TYPE(Enum):
	# 行情数据
	K_DAY='K_DAY'			# 日线
	K_TRDMIN='K_TRDMIN'		# 分时
	K_TAQ='K_TAQ'			# 分笔
	# 股票数据
	STOCK_FIN_BALANCE='STOCK_FIN_BALANCE'			# 财务数据
	STOCK_BASIC='STOCK_BASIC'
	# 板块数据
	PLATE_COMPONENT='PLATE_COMPONENT'  # 板块成分数据
	# 指数数据
	INDEX_BASIC='INDEX_BASIC'
	# 经济数据
	ECO_GDP='ECO_GDP'
class EXCHANGE(Enum):
	UNK='UNK'
	SHSE='SHSE'
	SZSE='SZSE'
# 数据组织方式枚举
class GROUP_BY_TYPE(Enum):
	UNK='UNK'
	FIELDS='Fields'
	CODE='Code'
	TIME='Time'
	DEFAULT='Default'
# RetReason枚举
class RET_REASON(Enum):
	UNK=''
# 数据来源枚举
class DATA_SOURCE(Enum):
	UNK='UNK'
	TUSHARE='Tushare'
	GTA_QTAPI='GTA_QTApi'
	SINA='Sina'
	SQLSERVER='SqlServer'
	LOCAL='Local'
	CYCLE_ALL='CycleAll'
# 空值枚举
class NONE_DATA(Enum):
	NONE_STR=''
	NONE_LIST=[]
	NONE=None
# EnumEnd----------------------------------
####################################### 类定义 #######################################################################
# 代码类
class FM_Code():
	def __init__(self):
		self.Code=''
		self.Exchange=''
		self.FullCode=''
# 时间类
class FM_TimeList():
	def __init__(self):
		self.Start=datetime.datetime(1970,1,1,0,0,0,0)
		self.End=datetime.datetime(1970,1,1,0,0,0,0)
		self.ToStr()
	def ToStr(self):
		self.StartStr=self.Start.strftime('%Y-%m-%d %H:%M:%S')
		self.EndStr=self.End.strftime('%Y-%m-%d %H:%M:%S')
		# self.StartDateStr=self.Start.strftime('%Y-%m-%d')
		# self.EndDateStr=self.End.strftime('%Y-%m-%d')
		# self.StartTimeStr=self.Start.strftime('%H:%M:%S')
		# self.EndTimeStr=self.End.strftime('%H:%M:%S')
# 数据类
class FM_Data():
	def __init__(self,DataList,DataListIndx,GroupByType):
		if type(DataList) is not list and type(DataList) is pd.DataFrame:
			DataList=[DataList]
			DataListIndx=[DataListIndx]
		# 初始化
		self.Value={}
		self.GroupByType=GroupByType
		self.ValueIndex=DataListIndx
		# 开始赋值
		for x in range(0,len(DataList)):
			self.Value[DataListIndx[x]]=DataList[x]
	def ReadData(self,DataList):
		# 推测识别列表数据的组织形式
		pass
		return self
# 返回结果类
class FM_Ret():
	def __init__(self,Ret,RetReason):
		self.Value=Ret
		self.RetReason=RetReason

####################################### 函数定义 #######################################################################
# 判断是不是枚举值成员
def IsEnumMember(Item,EnumGiven):
	RetValue=False
	if Item in [x.value for x in EnumGiven.__members__.values()]:
		RetValue=True
	return RetValue
# 获取枚举成员值
def GetEnumMember(EnumGiven):
	RetValue=[x.value for x in EnumGiven.__members__.values()]
	return RetValue

pass