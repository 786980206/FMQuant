#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'

WORK_PATH = 'E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta5.0'  # 工作目录
DATA_MOD_PATH=WORK_PATH+"\\DataMod"
PY_MOD_PATH=WORK_PATH+"\\PyMod"
################################################# 模块导入 ##############################################################
import sys
import json
import os
import pandas as pd
sys.path.append(WORK_PATH)
sys.path.append(DATA_MOD_PATH)
sys.path.append(PY_MOD_PATH)
import CommenUsedMod

# 根据Optio组成网页
def CombinChartHtml(Option,OutPath='Test.html',Mod=''):
	AimStr=''
	DomConfig='<div id="main" style="width: 1000px;height:600px;margin-left:auto;margin-right:auto;">'
	page_head='<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="utf-8">\n    <title>ECharts</title>\n    <!-- 引入 echarts.js -->\n    <script src="echarts.min.js"></script>\n</head>\n<body>\n    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->\n    '\
			  +DomConfig \
			  +'</div>\n    <script type="text/javascript">\n        // 基于准备好的dom，初始化echarts实例\n        var myChart = echarts.init(document.getElementById(\'main\'));\n\n        // 指定图表的配置项和数据\n'
	page_tail=';\n\n        // 使用刚指定的配置项和数据显示图表。\n        myChart.setOption(option);\n    </script>\n</body>\n</html>'
	if Mod=='':
		if type(Option)==str:
			AimStr=page_head+'        var option ='+Option+page_tail
		elif type(Option)==dict:
			Option=json.dumps(Option)
			AimStr=page_head+'        var option ='+Option+page_tail
	elif Mod=='file':
		Option=CommenUsedMod.ReadFile(Option,encoding=None)
		AimStr=page_head+Option+page_tail
	CommenUsedMod.WriteFile(AimStr,OutPath)
# 读取保存到回测记录
ResultPath=r'E:\OneDrive\0_Coding\010_MyQuantSystem\Beta5.0\Strategy\OpenAndCloseStg_BackTestResult\20180615175026'
ChromePath=r'E:\GoogleChromePortable64\GoogleChromePortable.exe'
# ChromePath=r'C:\Users\fengming.liu\AppData\Local\Google\Chrome\Application\chrome.exe'
class AccPerf(object):
	def __init__(self,ResultPath,AccIndex):
		self.CashRec=pd.DataFrame.from_csv(ResultPath+'\\'+str(AccIndex)+"_CashRec.csv")
		self.Position=pd.DataFrame.from_csv(ResultPath+'\\'+str(AccIndex)+"_Position.csv")
		self.DealRec=pd.DataFrame.from_csv(ResultPath+'\\'+str(AccIndex)+"_DealRec.csv")
		self.OrderRec=pd.DataFrame.from_csv(ResultPath+'\\'+str(AccIndex)+"_OrderRec.csv")
		self.Order=pd.DataFrame.from_csv(ResultPath+'\\'+str(AccIndex)+"_Order.csv")
# ChartOption类
class ChartOption(object):
	def __init__(self):
		self.title=None
		self.legend=None
		self.grid=None
		self.xAxis=None
		self.yAxis=None
		self.polar=None
		self.radiusAxis=None
		self.angleAxis=None
		self.radar=None
		self.dataZoom=None
		self.visualMap=None
		self.tooltip=None
		self.axisPointer=None
		self.toolbox=None
		self.brush=None
		self.geo=None
		self.parallel=None
		self.parallelAxis=None
		self.singleAxis=None
		self.timeline=None
		self.graphic=None
		self.calendar=None
		self.dataset=None
		self.aria=None
		self.series=None
		self.color=None
		self.backgroundColor=None
		self.textStyle=None
		self.animation=None
		self.animationThreshold=None
		self.animationDuration=None
		self.animationEasing=None
		self.animationDelay=None
		self.animationDurationUpdate=None
		self.animationEasingUpdate=None
		self.animationDelayUpdate=None
		self.blendMode=None
		self.hoverLayerThreshold=None
		self.useUTC=None
	def to_dict(self):
		temp=self.__dict__.copy()
		for key,value in self.__dict__.items():
			if value==None:temp.pop(key)
		return temp

if __name__=='__main__':
	Data=AccPerf(ResultPath,0)
	A=ChartOption()
	A.title={'text':'资金曲线图', 'left':'center','subtext':ResultPath}
	A.xAxis={'type': 'category',
			'data': list(Data.CashRec['Time'])
			 }
	A.yAxis={'type': 'value' }
	A.series=[{'data': list(Data.CashRec['Cash']),'type': 'line','name':'Cash' },
			  {'data': list(Data.CashRec['CashAvailable']),'type': 'line' ,'name':'CashAvailable'},
			  {'data': list(Data.CashRec['TotalValue']),'type': 'line','name':'TotalValue' }]
	A.legend={'left': 'center',
			  'top':'bottom',
			  'data': ['Cash', 'CashAvailable','TotalValue']
			 }
	A.tooltip={'trigger': 'axis',
			   'axisPointer': {'type': 'cross'}
			   }
	A.dataZoom=[{'type':'inside','start':0,'end':100}]
	CombinChartHtml(A.to_dict())
	os.system(ChromePath+' '+os.getcwd()+'\\Test.html')


	Data=AccPerf(ResultPath,0)
	# CombinChartHtml('file.txt',Mod='file')

