# -*- coding: utf-8 -*-

'''
具体的策略的逻辑编写模块：
策略逻辑本身是：当前（及历史）所有的外部信息集和本身自己的信息集（账户信息等）共同作用做出决策的过程。
此外还有一些其他的设置项，就不在这里进行设置了，而在其他地方进行设置。

'''


# 这里策略的执行还是要分两种模式，主要是在策略驱动的部分实现：
# 1.指令立即生效模式
# 2.策略运行完再统一执行的模式
# 目的主要在于区别当前策略的下单等操作是否对当前策略后续决策产生影响。
def Main(AccounList,Data,Target):
	Code='000001.SZSE' #代码.交易所
	Direction=1 # 0：卖，1：买，-1：开空，2：平空
	Price=10.05
	Vol=100
	AddPar={}
	ret=AccounList[0].PlaceOrder(Code,Direction,Price,Vol,AddPar)
	OrderVol=AccounList[0].GetOrder(Code,Direction,Price,Vol)
	ret=AccounList[0].CancelOrder(OrdeVol)

	pass


if __name__=='__main__':
	import sys,os
	abspath=os.path.abspath(__file__)
	BasePath=os.path.abspath(os.path.join(os.path.dirname(abspath),'..','PyMod'))
	sys.path.add('BasePath')
	import Counter
	