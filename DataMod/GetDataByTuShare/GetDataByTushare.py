#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WindSing'
####################################### 一些说明 #######################################################################
# 获取历史数据的话，没有成交金额的话直接用get_k_data，有成交金额的话用get_h_data但是必须要按时间段取，不超过3年，按2年分段比较合理
# get_h_data的话date是index而get_k_data的date不是，get_k_data的速度快很多
# get_h_data:只支持日线
# get_hist_data:近三年的日线,最近350个分时数据(可以按时间段取)
# get_k_data:日线全部，分时只有最近482个数据(不能按时间段取)

# get_stock_basics
# 获取沪深上市公司基本情况
# Parameters
# date:日期YYYY-MM-DD，默认为上一个交易日，目前只能提供2016-08-09之后的历史数据

####################################### 导入模块 #######################################################################
import tushare as ts
import DataModify
import DataDef
from enum import Enum
import datetime
import pandas as pd
####################################### 常量定义 #######################################################################
K_DAY_FIELDS=['open','high','close','low','volume','amount']
# 这个变量用于把标准化的FIELDS转化成Tushare能识别的变量
TUSHARE_K_DAY_TRAN_FIELDS={DataDef.FIELDS_K_DAY.OP.value:'open',
						   DataDef.FIELDS_K_DAY.HP.value:'high',
						   DataDef.FIELDS_K_DAY.CP.value:'close',
						   DataDef.FIELDS_K_DAY.LP.value:'low',
						   DataDef.FIELDS_K_DAY.VOL.value:'volume',
						   DataDef.FIELDS_K_DAY.Amount.value:'amount'
						   }
TUSHARE_STOCK_BASIC_TRAN_FIELDS={DataDef.FIELDS_STOCK_BASIC.Code.value:'code',      # 代码
							DataDef.FIELDS_STOCK_BASIC.Name.value:'name',      # 名称
							DataDef.FIELDS_STOCK_BASIC.Plate_Industry.value:'industry',       # 细分行业
							DataDef.FIELDS_STOCK_BASIC.Plate_Area.value:'area',      # 地区
							DataDef.FIELDS_STOCK_BASIC.PE.value:'pe',        # 市盈率
							DataDef.FIELDS_STOCK_BASIC.Shares_Tradable.value:'outstanding',         # 流通股本
							DataDef.FIELDS_STOCK_BASIC.Shares_Total.value:'totals',         # 总股本(万)
							DataDef.FIELDS_STOCK_BASIC.Assets_Total.value:'totalAssets',         # 总资产(万)
							DataDef.FIELDS_STOCK_BASIC.Assets_Liquid.value:'liquidAssets',        # 流动资产
							DataDef.FIELDS_STOCK_BASIC.Assets_Fixed.value:'fixedAssets',         # 固定资产
							DataDef.FIELDS_STOCK_BASIC.Reserved.value:'reserved',       # 公积金
							DataDef.FIELDS_STOCK_BASIC.Reserved_PerShare.value:'reservedPerShare',         # 每股公积金
							DataDef.FIELDS_STOCK_BASIC.EPS.value:'esp',       # 每股收益
							DataDef.FIELDS_STOCK_BASIC.BVPS.value:'bvps',      # 每股净资
							DataDef.FIELDS_STOCK_BASIC.PB.value:'pb',        # 市净率
							DataDef.FIELDS_STOCK_BASIC.Time_toMarket.value:'timeToMarket'        # 上市日期
							}
####################################### 函数定义 #######################################################################
# 最主要的提取数据的函数
def Get_K_DAY_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	# 这里传过来的参数和字段时间轴等都是规则化之后的了，这部分需要加上接独特的处理
	# 暂时没有处理
	for TempCode in CodeList:
		if 'Amount' not in Fields:
			RetValue.append(ts.get_k_data(TempCode.Code,TimeList.StartStr,TimeList.EndStr))
		else:
			try:
				RetValue.append(ts.get_h_data(TempCode.Code,TimeList.StartStr,TimeList.EndStr))
			except:
				Fields=Fields.remove('Amount')
				print('可能由于提取时间过长，tushare.get_h_data失败，尝试换成tushare.get_k_data')
				RetValue.append(ts.get_k_data(TempCode.Code,TimeList.StartStr,TimeList.EndStr))
	# Tushare两种不同的方式可能提取的数据可能不是以时间为Index的，设置一下
	try:
		for x in range(0,len(RetValue)):RetValue[x]=RetValue[x].set_index('date')
		# RetValue=[x.set_index('date') for x in RetValue]
	except:
		pass
	# 数据提取完毕，再取相应字段
	Fields=[x for x in Fields if x in TUSHARE_K_DAY_TRAN_FIELDS.keys()]
	TempFields=[TUSHARE_K_DAY_TRAN_FIELDS[x] for x in Fields]
	for x in range(0,len(RetValue)):
		try:
			RetValue[x]=RetValue[x][TempFields]
			RetValue[x].columns=Fields
			RetValue[x].index.name='Time'
		except:
			pass
	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,[x.FullCode for x in CodeList],DataDef.GROUP_BY_TYPE.CODE.value)
	return Ret,RetValue
# 取到STOCK_BASIC的处理
def Get_STOCK_BASIC_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	# 这里传过来的参数和字段时间轴等都是规则化之后的了，这部分需要加上接独特的处理
	# 由于Tushare默认是取上一个交易日的，所以TimeList默认加一
	TempTime=TimeList.Start+datetime.timedelta(days=1)
	# Code是Index,默认去掉
	if 'Code' in Fields:Fields.remove('Code')
	# 暂时没有处理
	RetValue=ts.get_stock_basics(TempTime.date().isoformat())
	# 数据提取完毕，先取相应代码
	try:
		TempCode=[x.Code for x in CodeList]
		RetValue=RetValue.loc[TempCode]
	except:
		Ret.Value=DataDef.STATUS.FAIL.value
		Ret.RetReason='获取相应代码失败'
	# 数据提取完毕，再取相应字段
	Fields=[x for x in Fields if x in TUSHARE_STOCK_BASIC_TRAN_FIELDS.keys()]
	TempFields=[TUSHARE_STOCK_BASIC_TRAN_FIELDS[x] for x in Fields]
	RetValue=RetValue[TempFields]
	RetValue.columns=Fields
	RetValue.index.name='Code'
	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,TimeList.StartStr,DataDef.GROUP_BY_TYPE.TIME.value)
	return Ret,RetValue
# 取全部字段的处理
def GetAllFields(DataType):
	if DataType==DataDef.DATA_TYPE.K_DAY.value:
		RetValue=list(TUSHARE_K_DAY_TRAN_FIELDS.keys())
		RetValue.remove('Amount')
	elif DataType==DataDef.DATA_TYPE.STOCK_BASIC.value:
		RetValue=list(TUSHARE_STOCK_BASIC_TRAN_FIELDS.keys())
	return RetValue

######################################## 主程序 ########################################################################
if __name__=='__main__':
	# A,B=Get_K_DAY_Data(DataModify.CodeListModify(['000001','600000']),DataModify.TimeListModify(['2018-01-01','2018-02-01']),['CP'])
	C,D=Get_STOCK_BASIC_Data(DataModify.CodeListModify(['000001','600000']),DataModify.TimeListModify('20180204'),['Code','Name'])
	pass