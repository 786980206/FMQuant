#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'
WORK_PATH = 'E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta3.0 with Data Extraction'  # 工作目录

import sys
import random
import pandas as pd

'''
                000001.SZSE 600000.SHSE
CP                    11.33        17.8
VOL                56349787    42240610
Price_LimitUp         13.19        20.1
OP                       12       18.28
LP                    11.23       17.55
Price_LimitDown       10.79       16.44
HP                    12.03       18.28;
                000001.SZSE 600000.SHSE
CP                     11.4       17.96
VOL                66326995    58054793
Price_LimitUp         12.46       19.58
OP                    11.27       17.51
LP                    11.15        17.4
Price_LimitDown        10.2       16.02
HP                    11.57       18.06;
Slippage=0.001
CostRatio=0.0005
MarketPartcipation=0.5
InitCash=1000000
'''

def Main(QuoteData,HisData,Account):
	# 1 验单
	# 1.1 大于涨停价
	Account[0].PlaceOrder('000001.SZSE',1,99,100)
	# 1.2 小于跌停价
	Account[0].PlaceOrder('000001.SZSE',1,1,100)
	# 1.3 可用资金不足
	Account[0].PlaceOrder('000001.SZSE',1,0,90000)
	# 1.4 可用持仓不足
	Account[0].PlaceOrder('000001.SZSE',0,0,100)
	# 2 撮合
	# 2.1 市价多
	Account[0].PlaceOrder('000001.SZSE',1,0,100)
	# 2.2 限价多
	Account[0].PlaceOrder('000001.SZSE',1,12,100)
	# 2.3 市价平多
	Account[0].PlaceOrder('000001.SZSE',0,0,100)
	# 2.4 限价平多
	Account[0].PlaceOrder('000001.SZSE',0,11,100)
	# 2.5 部分成交
	Account[0].PlaceOrder('000001.SZSE',1,0,6000)
	# 2.6 等待成交
	Account[0].PlaceOrder('000001.SZSE',1,10.80,100)



if __name__=='__main__':
	import sys
	sys.path.append('E:\\OneDrive\\0_Coding\\010_MyQuantSystem\\Beta2.0\\Strategy')