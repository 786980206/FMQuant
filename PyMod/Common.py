# -*- coding=utf-8 -*-

# 根据代码获取交易所信息
def GetExchangeByCode(Code):
	Exchange=Code.split('.')[1]
	return Exchange