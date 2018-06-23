#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'


################################################# 模块导入 ##############################################################
import sys
import CounterMod
import EventMod
import pandas as pd
import GeneralMod

################################################ 变量定义 ###############################################################
# 常量
STG_CONFIG_SPEC_PATH="..\\Setting\\StgConfigSpec.ini"  # 策略配置的定义文件
# 其他
Log=GeneralMod.Log()

################################################ 类定义 ###############################################################
class Strategy(object):
    def __init__(self,Path,Name,AccountConfig,QuoteDataConfig,HisDataConfig):
        sys.path.append(Path)
        # 绑定策略主函数
        exec('import '+Name)
        exec('self.Run='+Name+'.Main')
        # 绑定策略账户
        self.Account=[]
        for TempAccount in AccountConfig:
            if TempAccount!="AccountNum":
                self.Account.append(CounterMod.Account(Type=AccountConfig[TempAccount]))
        self.QuoteDataConfig=QuoteDataConfig
        self.HisDataConfig=HisDataConfig
        # 记录策略信息
        self.Path=Path
        self.Name=Name
    # 处理DataFeed事件
    def DealFeedData(self,Event_DataFeed):
        map(lambda x:x.Refresh(EventMod.Event(EventMod.EVENT_ORDERRETURN)),self.Account)
        # 判断是不是本策略的行情事件
        self.Run(Event_DataFeed.Value,'',self.Account)

################################################ 函数定义 ###############################################################
def LoadStrategy(StgConfig):
    StgConfigPath=StgConfig['StrategyFolder']+"\\"+StgConfig['StrategyName']+".ini"
    StrategyConfig=GeneralMod.LoadIni(StgConfigPath,STG_CONFIG_SPEC_PATH)
    TempStrategy=Strategy(StgConfig['StrategyFolder'],StgConfig['StrategyName'],StrategyConfig['AccountConfig'],StrategyConfig['QuoteDataConfig'],StrategyConfig['HisDataConfig'])
    return  TempStrategy,StrategyConfig['MatchConfig']

################################################ 主函数 #################################################################
if __name__=='__main__':
    pass
