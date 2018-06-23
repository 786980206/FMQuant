#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'
####################################### 一些说明 #######################################################################
#
####################################### 导入模块 #######################################################################
import datetime
from dateutil import parser
import pandas as pd
import DataDef
####################################### 常量定义 #######################################################################

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
		self.Start=datetime.datetime.now()
		self.End=datetime.datetime.now()
		self.ToStr()
	def ToStr(self):
		self.StartStr=self.Start.strftime('%Y-%m-%d %H:%M:%S')
		self.EndStr=self.End.strftime('%Y-%m-%d %H:%M:%S')
# 数据类
class FM_Data():
	def __init__(self,DataList,DataListIndex,GroupByType):
		if type(DataList) is not list and type(DataList) is pd.DataFrame:
			DataList=[DataList]
			DataListIndex=[DataListIndex]
		# 初始化
		self.Value={}
		self.GroupByType=GroupByType
		self.ValueIndex=DataListIndex
		# 开始赋值
		for x in range(0,len(DataList)):
			self.Value[DataListIndex[x]]=DataList[x]
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
# 代码规则化处理函数
def CodeModify(CodeStr):
	Temp=FM_Code()
	AimExchange='UNK'
	AimCode=''
	if '.' in CodeStr:
		TempCode,TempExchange=CodeStr.split('.')
		# 规则化交易所
		try:
			AimExchange=DataDef.TRAN_EXCHANGE[TempExchange.upper()]
		except:
			AimExchange='UNK'
		AimCode=TempCode
	else:
		AimCode=CodeStr
	# 输出类
	Temp.Code=AimCode
	Temp.Exchange=AimExchange
	Temp.FullCode=AimCode+'.'+AimExchange
	return Temp
def CodeListModify(CodeList):
	if not type(CodeList) is list:
		CodeList=[CodeList]
	Temp=[CodeModify(x) for x in CodeList]
	return Temp
# 字段规则化处理
def FieldsModify(Fields):
	if Fields=='All':return Fields
	if not type(Fields) is list:
		Fields=[Fields]
	Fields=[x.upper() for x in Fields]
	# 把能识别的转化了
	Fields=[DataDef.TRAN_FIELDS[x] for x in Fields if x in DataDef.TRAN_FIELDS.keys()]
	return Fields
# 时间规则化处理
def TimeListModify(TimeList):
	if DataDef.IsEnumMember(TimeList,DataDef.NONE_DATA):
		# 如果为空，直接返回
		return TimeList
	Temp=FM_TimeList()
	TempRet=['','']
	if type(TimeList) is list and len(TimeList)==2:
		TempRet=[parser.parse(x) for x in TimeList]
		# 输出类
		Temp.Start=TempRet[0]
		Temp.End=TempRet[1]
		Temp.ToStr()
	elif type(TimeList) is str and TimeList!='':
		TempRet=parser.parse(TimeList)
		Temp.Start=TempRet
		Temp.End=TempRet
		Temp.ToStr()
	return Temp
# 数据组织形式转化
def DataGroup(DataList,GroupByType):
	if type(DataList) is not FM_Data:
	# 识别数据当前z组织形式并转化成FM_Data
		DataList=FM_Data.ReadData(DataList)
	# 转化成新的组织形式
	if DataList.GroupByType==GroupByType or GroupByType==DataDef.GROUP_BY_TYPE.DEFAULT.value:
		return DataList
	elif GroupByType==DataDef.GROUP_BY_TYPE.TIME.value:
		# 只有按时间组织需要单独写
		pass
	else:
		# 另外两种只需要把FM_Data.Value[x].columns与FM_Data.ValueIndex交换即可
		TempRet=[]
		AimValueIndex=list(DataList.Value[DataList.ValueIndex[0]].columns)
		for TempColunm in AimValueIndex:
			TempSeries=pd.DataFrame()
			for TempIndex  in DataList.ValueIndex:
				if TempSeries.empty:
					TempSeries=DataList.Value[TempIndex][TempColunm]
				else:
					TempSeries=pd.concat([TempSeries,DataList.Value[TempIndex][TempColunm]],axis=1)
			TempSeries.columns=DataList.ValueIndex
			TempRet.append(TempSeries)
		TempRet=FM_Data(TempRet,AimValueIndex,GroupByType)
		return TempRet
# 参数规则化
def ParModify(CodeList,TimeList,Fields):
	CodeList=CodeListModify(CodeList)
	TimeList=TimeListModify(TimeList)
	Fields=FieldsModify(Fields)
	return CodeList,TimeList,Fields