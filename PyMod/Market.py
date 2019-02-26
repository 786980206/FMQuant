# -*- coding: utf-8 -*-

import pandas as pd

class MktSliNow(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass
	def GetDataByCode(self,Code,Item):
		if Item=='Price_LimitUp':return 15
		if Item=='Price_LimitDown':return 5
		if Item=='Price':return 10
		if Item=='Volume4Trd':return 500 # 获取Volume4Trd的时候要考虑市场参与度
		# Volume4Trd=math.floor(Volume4Trd/100)*100

	# 处理订单撮合（扣除市场成交量等）
	def DealMatchRet(self,OrderInfo,MatchInfo):
		return 1,''