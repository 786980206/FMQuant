#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'


# 导入模块
import sys
# sys.path.append('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta4.0')
import DataMod
import pandas as pd
import EventMod
import GeneralMod
import DataDef
import GetData as GD
Log=GeneralMod.Log()
# 定义类

## 数据类
## 目前是专指的时间序列数据，还在考虑对截面数据的支持
class Data(object):
	def __init__(self, DataName, TimeList,CodeList,Value=None, ParList=None):
		'''
		:param DataName: 对应字段
		:param TimeList: 时间列表
		:param CodeList: 代码列表
		:param Value: 具体数据
		:param ParList: 其他参数
		:return:
		'''
		self.DataName = DataName
		self.TimeList=TimeList
		self.CodeList=CodeList
		if Value is None:
			self.Value=pd.DataFrame()
		else:
			self.Value=Value
		if ParList is None:
			self.ParList={}
		else:
			self.ParList=ParList
	# 按时间添一行数据
	def addbyTime(self):
		pass
	# 按代码添一列数据
	def addbyCode(self):
		pass

# 定义函数
def GetData(Fields,StartTime,EndTime,CodeList,DataPar=None):
	'''
	:param Fields:
	:param StartTime:
	:param EndTime:
	:param CodeList:
	:param DataPar：包括｛'TimeInterval':'1Day','PriceAdj':'Backward','DataSource':'Local'｝
	:return:
	- Temp_Data：一个列表，内部每个元素为一个Data类
	- ItemList：一个列表，每个元素为对应的字段名称
	- TimeList：提取数据的时间列表
	'''
	TimeList=[StartTime,EndTime]
	# a.识别参数
	if DataPar is None:
		DataPar={}
	# a.1 数据类型
	if 'DataType' not in DataPar:
		DataPar['DataType']=DataDef.DATA_TYPE.K_DAY.value
	# a.2 组织方式
	if 'GroupByType' not in DataPar:
		DataPar['GroupByType']=DataDef.GROUP_BY_TYPE.FIELDS.value
	# a.3 数据来源
	# 留坑待补，这是为了整合市面上不同数据接口，也支持本地，理想中可以用一个配置文件控制提取的先后顺序，保证获取到数据
	if 'DataSource' not in DataPar:
		DataPar['DataSource']=DataDef.DATA_SOURCE.GTA_QTAPI.value # 目前这里以采用QTAPI的接口为主
	# b.取数
	Ret,RetValue=GD.GetData(CodeList,TimeList,Fields,DataPar['DataType'],DataPar['GroupByType'],DataPar['DataSource'],SpecialConfig={})
	return RetValue.Value,RetValue.ValueIndex,list(RetValue.Value[RetValue.ValueIndex[0]].index)

def GetDataByField(Field,StartTime,EndTime,CodeList,TimeInterval,PriceAdj,DataSource):
	if Field=='CP':
		temp=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\CP.csv')
		temp_TimeList=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\TimeList.csv')
		temp=temp.set_index(temp_TimeList['TimeList'])
		Temp_Data=Data(Field,temp_TimeList,CodeList,temp,{'TimeInterval':TimeInterval,'PriceAdj':PriceAdj,'DataSource':DataSource})
	elif Field=='CQ':
		temp=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\CQ.csv')
		temp_TimeList=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\TimeList.csv')
		temp=temp.set_index(temp_TimeList['TimeList'])
		Temp_Data=Data(Field,temp_TimeList,CodeList,temp,{'TimeInterval':TimeInterval,'PriceAdj':PriceAdj,'DataSource':DataSource})
	elif Field=='HardenPrice':
		temp=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\CP.csv')
		temp_TimeList=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\TimeList.csv')
		temp=temp.set_index(temp_TimeList['TimeList'])
		Temp_Data=Data(Field,temp_TimeList,CodeList,temp,{'TimeInterval':TimeInterval,'PriceAdj':PriceAdj,'DataSource':DataSource})
	elif Field=='DropStopPrice':
		temp=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\CP.csv')
		temp_TimeList=pd.read_csv('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\DataMod\\TimeList.csv')
		temp=temp.set_index(temp_TimeList['TimeList'])
		Temp_Data=Data(Field,temp_TimeList,CodeList,temp,{'TimeInterval':TimeInterval,'PriceAdj':PriceAdj,'DataSource':DataSource})

	else:
		Temp_Data='Error,Field:'+ Field + ' not find!'
	return Temp_Data

# 建立一个展示行情的函数，监听行情信息
def ShowData(Event_DataFeed):
	Log.debug("======================================================================新行情来啦======================================================================")
	Log.debug('Date=%s;CodeList=%s;Item=%s;Data=\n%s;' % (Event_DataFeed.Value['Date'],Event_DataFeed.Value['CodeList'],Event_DataFeed.Value['Item'],Event_DataFeed.Value['Data']))
# 建立一个模拟推送数据函数
def DataFeedSimulation(EventEngine,Fields,StartTime,EndTime,CodeList,Strategies,DataPar=None):
	# a.提取数据：目前考虑的是先全部提取，然后循环推送，以后数据量大了可能会考虑分段提取推送
	Data,ItemList,TimeList=GetData(Fields,StartTime,EndTime,CodeList,DataPar)
	for tempdate in TimeList.ix[:,'TimeList']:
		for tempcode in CodeList:
			DataFeedEvent=EventMod.Event(EventMod.EVENT_DATAFEED)
			DataFeedEvent.Value['Date']=tempdate
			DataFeedEvent.Value['Code']=tempcode
			DataFeedEvent.Value['Item']={}
			DataFeedEvent.Value['Strategies']=Strategies
			for tempitem in ItemList:
				DataFeedEvent.Value['Item'][tempitem]=Data[ItemList.index(tempitem)].Value.ix[tempdate,tempcode]
			# b.事件结构完成，开始加入引擎
			EventEngine.AddEvent(DataFeedEvent)

# a,b,c=GetData(['CP','CQ'],'00','00',['000001','600060'])
def DataFeed(Config):
	# 这里最终对接的是实时行情推送接口例如QTS，QTAPI等
	pass

if __name__=='__main__':
	# 在这里写一个模拟行情的过程，推送当事件处理引擎中去
	# a.初始化引擎
	CoreEventEngine=EventMod.EventEngine()
	# b.注册监听函数
	CoreEventEngine.Register(EventMod.EVENT_DATAFEED,ShowData)
	# c.启动引擎
	CoreEventEngine.Start()
	# d.开始模拟推送行情
	DataFeedSimulation(CoreEventEngine,['CP','CQ'],'','',['000001.SZSE','000060.SHSE'])
	# e.结束引擎
	CoreEventEngine.Stop()
	# python datamod\datamod.py

