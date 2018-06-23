#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'WindSing'


import pandas as pd
import math



def TradeSimulation(TempTradeInfo,Temp_Position,PriceData4Trade,VolumeData4Trade,BackTestPar):
    '''
    :param TempTradeInfo: 订单信息类，每一行对应的是[Exchange,Symbol,Price,Volume,Direction,AccountID]
    :param Temp_Position: 当前持仓信息，包括单一标的的状态和账户整体状态
    :param PriceData4Trade: 撮合价格数据，一行数据，行名称为对应时间，列名为对应标的
    :param VolumeData4Trade: 撮合成交量数据，一行数据，行名称为对应时间，列名为对应标的
    :param BackTestPar: 回测的参数信息等，包括交易成本，成交价格，滑点，市场参与度等
    :return:TradeRet：撮合的结果，DataFrame类型，就是在TempTradeInfo之上添加了成交价，成交量和备注等字段
    '''
    # 交易参数获取：交易成本，滑点，市场参与度，当前资金情况等等，先暂时不考虑
    __CostRatio=BackTestPar['TradeCostRatio']
    __CashAvailable=BackTestPar['CashAvailable']
    __Slippage=BackTestPar['Slippage']
    __MarketParticipation=BackTestPar['MarketPartcipation']

    # a.逐订单循环
    # a.1 初始化结果记录变量
    __TempRet=pd.DataFrame()
    # a.2 将成交量按市场参与度计算一下
    VolumeData4Trade=VolumeData4Trade*__MarketParticipation
    # a.3 开始循环
    for __temp in range(0,len(TempTradeInfo.Value)):
        # b.提取订单数据
        __TempTradeInfo=TempTradeInfo.Value.ix[__temp,:]
        # c.当前标的及下单账户
        __TempUnderLying=__TempTradeInfo['Symbol']+'.'+__TempTradeInfo['Exchange']
        __TempAccountID=__TempTradeInfo['AccountID']
        # d.成交价格比对
        # d.1 获取对应标的数据
        Price4Matching=PriceData4Trade[__TempUnderLying]
        if not Temp_Position.Value[__TempAccountID].empty:
            __VolumeAvaliable=Temp_Position.Value[__TempAccountID].ix[__TempUnderLying,['LongVolumeAvaliable','ShortVolumeAvaliable']]
        else:
            __VolumeAvaliable=pd.DataFrame([0,0]).T
            __VolumeAvaliable.columns=['LongVolumeAvaliable','ShortVolumeAvaliable']
            __VolumeAvaliable=__VolumeAvaliable.ix[0,:]
        # d.2 进行比对
        # d.2.1 市价开多仓
        if __TempTradeInfo['Price']==0 and __TempTradeInfo['Direction']==1:
            __PriceMatched=Price4Matching+__Slippage # 市价下多单，成交价为撮合价格加滑点
        # d.2.2 市价开空仓
        elif __TempTradeInfo['Price']==0 and __TempTradeInfo['Direction']==-1:
            __PriceMatched=Price4Matching-__Slippage # 市价下空单，成交价为撮合价格减滑点
        # d.2.3 限价开多仓
        elif (__TempTradeInfo['Price']>Price4Matching+__Slippage) and __TempTradeInfo['Direction']==1:
            __PriceMatched=Price4Matching+__Slippage # 限价下多单，成交价为撮合价格加滑点
        # d.2.4 限价开空仓
        elif (__TempTradeInfo['Price']<Price4Matching-__Slippage) and __TempTradeInfo['Direction']==-1:
            __PriceMatched=Price4Matching-__Slippage # 限价下空单，成交价为撮合价格减滑点
        # d.2.5 市价平多仓
        elif __TempTradeInfo['Price']==0 and __TempTradeInfo['Direction']==0:
            __PriceMatched=Price4Matching-__Slippage # 市价平多单，成交价为撮合价格减滑点
            if __VolumeAvaliable['LongVolumeAvaliable']<__TempTradeInfo['Volume']: # 持仓可用量不足
                __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Volume Avaliable not enough!',Price4Matching]).T]) # 成交不成功：持仓量不足
                continue
        # d.2.6 市价平空仓
        elif __TempTradeInfo['Price']==0 and __TempTradeInfo['Direction']==2:
            __PriceMatched=Price4Matching-__Slippage # 市价平空单，成交价为撮合价格加滑点
            if __VolumeAvaliable['ShortVolumeAvaliable']<__TempTradeInfo['Volume']:
                __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Volume Avaliable not enough!' ,Price4Matching]).T]) # 成交不成功：持仓量不足
                continue
        # d.2.7 限价平多仓
        elif (__TempTradeInfo['Price']>Price4Matching+__Slippage) and __TempTradeInfo['Direction']==0:
            __PriceMatched=Price4Matching-__Slippage # 限价平多单，成交价为撮合价格减滑点
            if __VolumeAvaliable['LongVolumeAvaliable']<__TempTradeInfo['Volume']:
                __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Volume Avaliable not enough!' ,Price4Matching]).T]) # 成交不成功：持仓量不足
                continue
        # d.2.8 限价平空仓
        elif (__TempTradeInfo['Price']<Price4Matching-__Slippage) and __TempTradeInfo['Direction']==2:
            __PriceMatched=Price4Matching+__Slippage # 限价平空单，成交价为撮合价格加滑点
            if __VolumeAvaliable['ShortVolumeAvaliable']<__TempTradeInfo['Volume']:
                __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Volume Avaliable not enough!' ,Price4Matching]).T]) # 成交不成功：持仓量不足
                continue
        else:
            __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Price didn\'t macthed!',Price4Matching ]).T]) # 成交不成功：价格原因
            continue # 跳出本次循环
        # e.成交量比对
        # e.1 获取对应标的数据
        __Volume4Matching=VolumeData4Trade[__TempUnderLying]
        # e.2 进行对比
        if math.floor(__Volume4Matching)==0:
            __VolumeMatched=0 # 当前没有成交量
            __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Volume didn\'t macthed!',Price4Matching ]).T]) # 成交不成功：成交量原因
            continue # 跳出向本次循环
        elif __TempTradeInfo['Volume']<math.floor(__Volume4Matching):
            __VolumeMatched=__TempTradeInfo['Volume'] # 全部成交
        elif __TempTradeInfo['Volume']>=math.floor(__Volume4Matching):
            __VolumeMatched=math.floor(__Volume4Matching) # 部分成交
        # f.资金情况的对比
        # f.1 开仓考虑资金情况
        if __TempTradeInfo['Direction']==1 or __TempTradeInfo['Direction']==-1:
            __CashMatched=__PriceMatched*__VolumeMatched*(1+__CostRatio)
            if __CashMatched>=__CashAvailable[__TempAccountID]:
                # 资金不足
                __TempRet=pd.concat([__TempRet,pd.DataFrame(['','','','Failed:Cash didn\'t macthed!',Price4Matching ]).T]) # 成交不成功：资金不足
                continue
            __CashAvailable[__TempAccountID]=__CashAvailable[__TempAccountID]-__CashMatched
        # f.2 平仓计算获取资金
        else:
            __CashMatched=__PriceMatched*__VolumeMatched*(1-__CostRatio)
            __CashAvailable[__TempAccountID]=__CashAvailable[__TempAccountID]+__CashMatched
        # g.成功撮合
        __TempRet=pd.concat([__TempRet,pd.DataFrame([__PriceMatched,__VolumeMatched,__CashMatched,'Successed',Price4Matching ]).T]) # 成交成功
        # g.1 对当前标的的成交量进行扣除
        VolumeData4Trade[__TempUnderLying]=VolumeData4Trade[__TempUnderLying]-__VolumeMatched
    # h.循环结束，对所有单都进行了撮合
    __TempRet.columns=['PriceMatched','VolumeMatched','CashMatched','MsgRet','PriceNow']
    __TempRet.index=TempTradeInfo.Value.index
    TotalRet=pd.concat([TempTradeInfo.Value,__TempRet],axis=1)
    return TotalRet

def DealFeedData(Event_DataFeed):
    # 这部分需要把行情数据和Account.Order连接起来，进行一个模拟撮合的操作
    # 如果是回测模式，会进行模拟撮合
    pass


if __name__=='__main__':
    # 以下函数用作测试
    pass



