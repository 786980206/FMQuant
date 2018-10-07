#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'
__ModName__ = "[Main]"

# 设置工作路径，以保证在任何目录下都可以运行
import os
import sys
PyMod=sys.path[0]
WORK_PATH = os.path.dirname(PyMod)  # 工作目录,上级目录
DataMod=WORK_PATH+"/DataMod"
CommonMod=WORK_PATH+"/CommonMod"
ChartMod=WORK_PATH+"/ChartMod"
sys.path.append(WORK_PATH)
sys.path.append(DataMod)
sys.path.append(PyMod)
sys.path.append(CommonMod)
sys.path.append(ChartMod)
################################################# 模块导入 ##############################################################
os.chdir(PyMod)
import time
import json
import pandas as pd
import EventMod
import TradeMod
import PushMod
import StrategyMod
import BackTestMod
import GeneralMod

pd.set_option('expand_frame_repr', False)
################################################ 变量定义 ###############################################################
CONFIG_FILE_PATH = "..\\Setting\\Config.ini"
CONFIG_SPEC_PATH = "..\\Setting\\ConfigSpec.ini"
CONFILE_FILE_PATH_JSON="../Setting/Config.json"
################################################ 主函数 #################################################################
def Main(WebObj=None):
	Log=GeneralMod.Log(AtFirst=True)
	# Log=GeneralMod.Log()
	# GeneralMod.LogWithColor('Test',Log.info,GeneralMod.FOREGROUND_RED) 这个写法是可以在终端上面显示颜色的！
	# time.sleep(10)
	# 系统开始
	# a.加载全部策略
	# a.1 获取系统参数
	# Config = GeneralMod.LoadIni(CONFIG_FILE_PATH, CONFIG_SPEC_PATH)
	Config = GeneralMod.LoadJson(CONFILE_FILE_PATH_JSON)
	# a.2 策略加载
	Strategy = StrategyMod.LoadStrategy(Config['StgConfig'])
	# b.初始化事件驱动引擎
	CoreEventEngine = EventMod.EventEngine()
	CoreEventEngine.Register(EventMod.EVENT_DATAFEED, PushMod.ShowData)
	if WebObj!=None:
		CoreEventEngine.Register(EventMod.EVENT_DATAFEED, WebObj.PushData)
	# c.初始化行情推送事件
	if Config['BackTestConfig']['ForBackTest']:
		MatchingSys = BackTestMod.MatchingSys(Strategy, CoreEventEngine, Config)
		# DataFeed需要绑定MatchingSys,因为回测的模拟撮合也是用到了这的行情，如果真实交易就不存在这个问题；
		DataFeed = BackTestMod.DataFeed(MatchingSys)
		CoreEventEngine.Register(EventMod.EVENT_DATAFEED,MatchingSys.RefreshQoutation)
	else:
		# 这里是真实交易的行情来源，所以是DataMod
		DataFeed = PushMod.DataFeed(Config['SubConfig'])
	# d.逐策略监听行情事件（DATAFEED）
	# map(lambda x:CoreEventEngine.Register(EventMod.EVENT_DATAFEED,x.DealFeedData),Strategies)
	CoreEventEngine.Register(EventMod.EVENT_DATAFEED, Strategy.DealFeedData)
	# d.1 监听订单回执事件（ORDERRETURN）
	# map(lambda x:CoreEventEngine.Register(EventMod.EVENT_ORDERRETURN,x.Account.Refresh),Strategies)
	# e.启动引擎
	CoreEventEngine.Start()
	# f.开始行情推送
	DataFeed.Run()
	# g.停止引擎
	while MatchingSys.IsRunning:
		# print(str(MatchingSys.IsRunning)+"------------------------------------------------")
		# 隔5s检测一次是否回测完成
		time.sleep(5)
	CoreEventEngine.Stop()
	MatchingSys.PerformanceStatistics()
	# print('----------------------over------------------------------------------------------------------')
	return

if __name__ =='__main__':
	Main()