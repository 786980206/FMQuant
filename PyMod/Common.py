# -*- coding=utf-8 -*-

# 根据代码获取交易所信息
def GetExchangeByCode(Code):
	try:
		if CheckCode(Code):
			Exchange=Code.split('.')[1]
			return Exchange
	except Exception as e:
		print(e)

# 校验交易代码
def CheckCode(Code):
	if type(Code) is not str:return 0
	if "." not in Code :return 0
	return 1