# -*- coding: utf-8 -*-

__author__ = 'WindSing'


################################################# 模块导入 ##############################################################
import sys
import CounterMod
import EventMod
import pandas as pd
import GeneralMod

################################################ 变量定义 ###############################################################
# 其他
Log=GeneralMod.Log()

################################################ 类定义 ###############################################################
class Strategy(object):
    def __init__(self,Path,Name,StrategyConfig):
        self.Path=Path
        self.Name=Name
        self.AccountConfig=StrategyConfig['AccountConfig']
        self.QuoteDataConfig=StrategyConfig['QuoteDataConfig']
        self.HisDataConfig=StrategyConfig['HisDataConfig']
        self.MatchConfig=StrategyConfig['MatchConfig']

        sys.path.append(self.Path)
        # 绑定策略主函数
        exec('import '+self.Name)
        exec('self.Run='+self.Name+'.Main')
        # 绑定策略账户
        self.Account=[]
        for TempAccount in self.AccountConfig:
            if TempAccount!="AccountNum":
                self.Account.append(CounterMod.Account(Type=self.AccountConfig[TempAccount]))
    # 处理DataFeed事件
    def DealFeedData(self,Event_DataFeed):
        map(lambda x:x.Refresh(EventMod.Event(EventMod.EVENT_ORDERRETURN)),self.Account)
        # 判断是不是本策略的行情事件
        self.Run(Event_DataFeed.Value,'',self.Account)

################################################ 函数定义 ###############################################################
def LoadStrategy(StgConfig):
    StgConfigPath=StgConfig['StrategyFolder']+"/"+StgConfig['StrategyName']+".json"
    StrategyConfig=GeneralMod.LoadJson(StgConfigPath)
    TempStrategy=Strategy(StgConfig['StrategyFolder'],StgConfig['StrategyName'],StrategyConfig)
    return  TempStrategy

################################################ 主函数 #################################################################
if __name__=='__main__':
    pass
