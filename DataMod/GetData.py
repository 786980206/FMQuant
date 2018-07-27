#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WindSing'
####################################### 一些说明 #######################################################################

####################################### 导入模块 #######################################################################
import sys
import os
import datetime
import time
import codecs
import DataModify
import DataDef
import CommenUsedMod
####################################### 常量定义 #######################################################################
# ----------------------------------------------------------------------------------------
# 可以获取数据的方式
from GetDataByTuShare import GetDataByTushare
from GetDataByGTA_QTApi import GetDataByGTA_QTApi
from GetDataBySqlServer import GetDataBySqlServer
# 数据来源的模块映射
DATA_SOURCE_LIST={DataDef.DATA_SOURCE.TUSHARE.value:GetDataByTushare,
				  DataDef.DATA_SOURCE.GTA_QTAPI.value:GetDataByGTA_QTApi,
				  DataDef.DATA_SOURCE.SQLSERVER.value:GetDataBySqlServer
				  }
# 数据来源的默认排序
DATA_SOURCE_CYCLE_LIST=[DATA_SOURCE_LIST['Tushare']]
####################################### 函数定义 #######################################################################
# 主要的取数据函数
def GetData(CodeList,TimeList=None,Fields='All',DataType=DataDef.DATA_TYPE.K_DAY.value,GroupByType=DataDef.GROUP_BY_TYPE.DEFAULT.value,DataSource=DataDef.DATA_SOURCE.CYCLE_ALL.value,SpecialConfig={}):
	RetValue=[]
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	# 参数规则化,转化为MySys的参数
	CodeList,TimeList,Fields=DataModify.ParModify(CodeList,TimeList,Fields)
	# 按照不同的数据类型提取数据
	# SpecialConfig={}
	if DataType==DataDef.DATA_TYPE.K_DAY.value:
		Ret,RetValue=Get_K_DAY_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource)
	elif DataType==DataDef.DATA_TYPE.STOCK_BASIC.value:
		Ret,RetValue=Get_STOCK_BASIC_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource)
	elif DataType==DataDef.DATA_TYPE.PLATE_COMPONENT.value:
		Ret,RetValue=Get_PLATE_COMPONENT_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource)
	RetValue=DataModify.DataGroup(RetValue,GroupByType)
	return Ret,RetValue
# 取到K_DAY数据的函数
def Get_K_DAY_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource):
	# 如果没有指定数据源头，循环DATA_SOURCE_CYCLE_LIST提数
	Ret.Value=DataDef.STATUS.FAIL.value
	if DataSource==DataDef.DATA_SOURCE.CYCLE_ALL.value:
		for TempSource in DATA_SOURCE_CYCLE_LIST:
			if Fields=='All':Fields=TempSource.GetAllFields(DataDef.DATA_TYPE.K_DAY.value)
			Ret,RetValue=TempSource.Get_K_DAY_Data(CodeList,TimeList,Fields,SpecialConfig)
			if Ret.Value:
				break
	# 如果指定了数据源头
	else:
		TempSource=DATA_SOURCE_LIST[DataSource]
		if Fields=='All':Fields=TempSource.GetAllFields(DataDef.DATA_TYPE.K_DAY.value)
		Ret,RetValue=TempSource.Get_K_DAY_Data(CodeList,TimeList,Fields,SpecialConfig)
	return Ret,RetValue
# 取到Get_STOCK_BASIC_Data数据的函数
def Get_STOCK_BASIC_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource):
	# 如果没有指定数据源头，循环DATA_SOURCE_CYCLE_LIST提数
	Ret.Value=DataDef.STATUS.FAIL.value
	if DataSource==DataDef.DATA_SOURCE.CYCLE_ALL.value:
		for TempSource in DATA_SOURCE_CYCLE_LIST:
			if Fields=='All':Fields=TempSource.GetAllFields(DataDef.DATA_TYPE.STOCK_BASIC.value)
			Ret,RetValue=TempSource.Get_STOCK_BASIC_Data(CodeList,TimeList,Fields,SpecialConfig)
			if Ret.Value:
				break
	else:
		TempSource=DATA_SOURCE_LIST[DataSource]
		if Fields=='All':Fields=TempSource.GetAllFields(DataDef.DATA_TYPE.STOCK_BASIC.value)
		Ret,RetValue=TempSource.Get_STOCK_BASIC_Data(CodeList,TimeList,Fields,SpecialConfig)
	return Ret,RetValue
def Get_PLATE_COMPONENT_Data(RetValue,Ret,CodeList,TimeList,Fields,SpecialConfig,DataSource):
	pass
def GetDataThroughStr(ParStr):
	Ret=DataDef.STATUS.SUCCESS.value
	RetValue=[]
	ParStr=ParStr[0:ParStr.find('---')]
	ParStrList=ParStr.replace("\n",",")
	Ret,RetValue=eval("GetData("+ParStrList+")")
	return Ret,RetValue

######################################## 主程序 ########################################################################
if __name__=='__main__':
	# try:
	GetDataPar=sys.argv
	# A,B=GetData([], [], ['Symbol', 'Market', 'ShortName'], 'STOCK_BASIC', 'Default', 'GTA_QTApi', {'GTA_QTApi_PLATE_ID': '1010001'})
	# GetDataPar=[0,r"E:\OneDrive\0_Coding\010_MyQuantSystem\Beta4.0\DataMod\Gui\Cache\CodeSelect.gd"]
	# GetDataPar=[0,r"E:\OneDrive\0_Coding\010_MyQuantSystem\Beta3.0\DataMod\Gui\Cache\TaskList.gd"]
	#  4Test
	# GetData(["000001.SZ","600000.sh"], ["20180101","20180201"],'All', 'K_DAY', 'Default', 'GTA_QTApi', {'GTA_QTApi_PLATE_ID2': '1010001','GTA_QTApi_PRICE_ADJUST':'k_AdjForward'})
	#  4Test
	GetDataFile=CommenUsedMod.ReadFile(GetDataPar[1],encoding='utf-8-sig')
	GetDataList=GetDataFile.split("\nGetDataStart:\n")
	# 如果没有指定具体文件，则按时间，按任务，按组织方式建立目录文件
	if os.path.split(GetDataList[0])[1]=='':
		TempPath=os.path.split(GetDataList[0])[0]+"\\"+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		# 目前的相对路径在GetDataBy_GTA_QTApi下面
		CommenUsedMod.WriteFile(TempPath,r"../Gui/Cache/TaskSavePath.tmp")
		for ListNum in range(1,len(GetDataList)):
			Ret,RetValue=GetDataThroughStr(GetDataList[ListNum])
			# 创建任务文件夹
			if os.path.isdir(TempPath+"\\Task"+str(ListNum))==False:
				os.makedirs(TempPath+"\\Task"+str(ListNum))
			for TempValueIndex in RetValue.ValueIndex:
				TempFileName=CommenUsedMod.checkNameValid(TempValueIndex)
				RetValue.Value[TempValueIndex].to_csv(TempPath+"\\Task"+str(ListNum)+"\\"+TempFileName+".csv",encoding="utf-8")
			CommenUsedMod.WriteFile("Task"+str(ListNum)+" Success\n",r"../Gui/Cache/TaskRet.tmp",'a+')
	else:
		Ret,RetValue=GetDataThroughStr(GetDataList[1])
		RetValue.Value[RetValue.ValueIndex[0]].to_csv(GetDataList[0],encoding="utf-8")
