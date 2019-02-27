# -*- coding: utf-8 -*-

import pandas as pd

class MktSliNow(object):
	"""docstring for ClassName"""
	def __init__(self,Data={'Price_LimitUp':15,'Price_LimitDown':5,'Price':10,'Volume4Trd':500}):
		self.Data=Data
	def GetDataByCode(self,Code,Item):
		# 获取Volume4Trd的时候要考虑市场参与度
		# Volume4Trd=math.floor(Volume4Trd/100)*100
		return self.Data[Item]

	# 处理订单撮合（扣除市场成交量等）
	def DealMatchRet(self,Code,MatchInfo):
		return 1,''