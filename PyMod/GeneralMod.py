#coding=gbk
__author__ = 'WindSing'

################################################# 模块导入 ##############################################################
import logging
import logging.config
import ctypes
import json
import os
import numpy as np
FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
STD_OUTPUT_HANDLE= -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

import pandas as pd
pd.set_option('expand_frame_repr', False)

################################################ 变量定义 ###############################################################
#  常量
LOG_CONFIG_PATH='..\\Setting\\Log.ini'
BASE_SETTING_FILE='..\\Setting\\ExchangeServerSetting.json'
BASE_LOGGINF_SETTING="""
    {
        "version":1,
        "formatters":{
            "fmt":{
                "format":"[%(asctime)s][%(name)s][%(levelname)s][%(filename)s][%(threadName)s][%(module)s][%(funcName)s][%(lineno)d] %(message)s",
                "datefmt":"%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers":{
            "consoleHandler":{
                "class":"logging.StreamHandler",
                "formatter":"fmt",
                "level":"DEBUG",
                "stream":"ext://sys.stdout"
            },
            "fileHandler":{
                "class":"logging.handlers.RotatingFileHandler",
                "formatter":"fmt",
                "level":"DEBUG",
                "filename":"../Log/PyMod.log",
                "mode":"a",
                "maxBytes":52428800,
                "backupCount":20,
                "encoding":"utf-8"
            }
        },
        "loggers":{
            "ExchangeServerLogger":{
                "level":"DEBUG",
                "handlers":["consoleHandler","fileHandler"]
            }
    
        }		
    }
"""

################################################ 函数定义 ###############################################################
# 加载配置文件的函数-----------------------------------------------------------------
def LoadJsonFile(FilePath):
    FilePath=PathJoin(FilePath)
    with open(FilePath) as f:
        ret=json.load(f)
    return ret

def LoadJsonStr(Str):
    try:
        ret=json.loads(Str)
    except:
        print("Json转化失败：{}".format(Str))
        ret=None
    return ret
# 保存配置文件的函数-----------------------------------------------------------------
def SaveJsonFile(FilePath,Data):
    FilePath=PathJoin(FilePath)
    str=json.dumps(Data)
    with open(FilePath,"w") as f:
        f.write(str)

def LoadJsonStr(Str):
    try:
        ret=json.loads(Str)
    except:
        print("Json转化失败：{}".format(Str))
        ret=None
    return ret

# 日志显示函数，可以通过改这里实现日志输出形式的变化-------------------------------
class Log(object):
    # 初始化
    def __init__(self,logger):
        self.logger=logger
        self.color=[FOREGROUND_WHITE,FOREGROUND_WHITE,FOREGROUND_BLUE,FOREGROUND_YELLOW,FOREGROUND_RED]
    # 设置显示颜色
    def set_color(self,color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
    # 带颜色输出日志
    def LogWithColor(self,Msg, Func, Color):
        self.set_color(Color)
        Func(Msg)
        self.set_color(FOREGROUND_WHITE)
    # 以下为日志函数
    def Debug(self,Msg):
        self.LogWithColor(Msg,self.logger.debug,self.color[0])
    def Info(self,Msg):
        self.LogWithColor(Msg,self.logger.info,self.color[1])
    def Warn(self,Msg):
        self.LogWithColor(Msg,self.logger.warning,self.color[2])
    def Error(self,Msg):
        self.LogWithColor(Msg,self.logger.error,self.color[3])
    def Critical(self,Msg):
        self.LogWithColor(Msg,self.logger.critical,self.color[4])


# 路径相关函数
# 获取当前目录
def GetCurrentPath():
    return os.getcwd()

# 目录拼接
def PathJoin(path, *paths):
    return os.path.abspath(os.path.join(path,*paths))

# 判断文件或目录还在不在
def PathConfirm(Path):
    Path=PathJoin(Path)
    return  os.path.exists(Path)

# 定义一个Json序列化类对Numpy处理
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

# 把Json等对象转化成str的函数
def ToStr(Item)->str:
    if type(Item) is dict:
        ret=Item
        ret=json.dumps(ret,cls=NpEncoder)
    else:
        ret=str(Item)
    return ret

# 构造发送消息的函数
def MakeSendMsg(Msg):
    Msg=ToStr(Msg)
    # print("发送消息：{}".format(Msg))
    Msg="Msg:" + Msg + "|End"
    return Msg

# 构造解析消息的函数
def AnalyzeMsg(MsgBefore,RecData):
    Msg = MsgBefore + RecData
    TempMsgList = Msg.split('|End')
    MsgList = TempMsgList[0:-1]
    MsgAfter = TempMsgList[-1]
    MsgList=[LoadJsonStr(x[4:]) for x in MsgList if x[0:4]=='Msg:']
    # print("接收消息：{}".format(MsgList))
    return MsgList,MsgAfter

################################################ 其他变量 #################################################################
FilePath=LoadJsonFile(BASE_SETTING_FILE)["ExchangeServerSetting"]["LoggingConfigFile"]
setting=LoadJsonFile(FilePath) if PathConfirm(FilePath) else BASE_LOGGINF_SETTING
logging.config.dictConfig(setting)
ExchangeServerLogger=logging.getLogger("ExchangeServerLogger")
ClientLogger=logging.getLogger("ClientLogger")
GuiLogger=logging.getLogger("GuiLogger")

################################################ 主函数 #################################################################
if __name__ =='__main__':
    print(PathConfirm("..\PyMod"))
    # ExchangeServerLogger.Debug("XXX")
    # ExchangeServerLogger.Warn("XXX")
    # ExchangeServerLogger.Error("XXX")
