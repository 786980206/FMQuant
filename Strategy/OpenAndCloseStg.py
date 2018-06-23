#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'
WORK_PATH = 'E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta3.0 with Data Extraction'  # 工作目录

import sys
import random
import pandas as pd

def Main(QuoteData,HisData,Account):
	# 策略很简单，查询持仓，有就卖，没就买
	Position=Account[0].GetPosition('000001.SZSE','Vol')
	# 要注意，这里返回的始终是一个pandas对象
	if Position[0]!=0:
		Account[0].PlaceOrder('000001.SZSE',0,0,100)
	else:
		Account[0].PlaceOrder('000001.SZSE',1,0,100)
	# Account[0].PlaceOrder('000001.SZSE',random.randint(0,1),0,random.randint(0,100)*100)
	# Account[0].PlaceOrder('000001.SZSE',1,0,1000000000)
	# Account[0].PlaceOrder('000001.SZSE',1,0,1000000000)


if __name__=='__main__':
	import sys
	sys.path.append('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\Strategy')