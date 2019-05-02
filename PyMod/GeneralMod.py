#coding=gbk
__author__ = 'WindSing'

################################################# ģ�鵼�� ##############################################################
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

################################################ �������� ###############################################################
#  ����
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

################################################ �������� ###############################################################
# ���������ļ��ĺ���-----------------------------------------------------------------
def LoadJsonFile(FilePath):
    FilePath=PathJoin(FilePath)
    with open(FilePath) as f:
        ret=json.load(f)
    return ret

def LoadJsonStr(Str):
    try:
        ret=json.loads(Str)
    except:
        print("Jsonת��ʧ�ܣ�{}".format(Str))
        ret=None
    return ret
# ���������ļ��ĺ���-----------------------------------------------------------------
def SaveJsonFile(FilePath,Data):
    FilePath=PathJoin(FilePath)
    str=json.dumps(Data)
    with open(FilePath,"w") as f:
        f.write(str)

def LoadJsonStr(Str):
    try:
        ret=json.loads(Str)
    except:
        print("Jsonת��ʧ�ܣ�{}".format(Str))
        ret=None
    return ret

# ��־��ʾ����������ͨ��������ʵ����־�����ʽ�ı仯-------------------------------
class Log(object):
    # ��ʼ��
    def __init__(self,logger):
        self.logger=logger
        self.color=[FOREGROUND_WHITE,FOREGROUND_WHITE,FOREGROUND_BLUE,FOREGROUND_YELLOW,FOREGROUND_RED]
    # ������ʾ��ɫ
    def set_color(self,color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
    # ����ɫ�����־
    def LogWithColor(self,Msg, Func, Color):
        self.set_color(Color)
        Func(Msg)
        self.set_color(FOREGROUND_WHITE)
    # ����Ϊ��־����
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


# ·����غ���
# ��ȡ��ǰĿ¼
def GetCurrentPath():
    return os.getcwd()

# Ŀ¼ƴ��
def PathJoin(path, *paths):
    return os.path.abspath(os.path.join(path,*paths))

# �ж��ļ���Ŀ¼���ڲ���
def PathConfirm(Path):
    Path=PathJoin(Path)
    return  os.path.exists(Path)

# ����һ��Json���л����Numpy����
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

# ��Json�ȶ���ת����str�ĺ���
def ToStr(Item)->str:
    if type(Item) is dict:
        ret=Item
        ret=json.dumps(ret,cls=NpEncoder)
    else:
        ret=str(Item)
    return ret

# ���췢����Ϣ�ĺ���
def MakeSendMsg(Msg):
    Msg=ToStr(Msg)
    # print("������Ϣ��{}".format(Msg))
    Msg="Msg:" + Msg + "|End"
    return Msg

# ���������Ϣ�ĺ���
def AnalyzeMsg(MsgBefore,RecData):
    Msg = MsgBefore + RecData
    TempMsgList = Msg.split('|End')
    MsgList = TempMsgList[0:-1]
    MsgAfter = TempMsgList[-1]
    MsgList=[LoadJsonStr(x[4:]) for x in MsgList if x[0:4]=='Msg:']
    # print("������Ϣ��{}".format(MsgList))
    return MsgList,MsgAfter

################################################ �������� #################################################################
FilePath=LoadJsonFile(BASE_SETTING_FILE)["ExchangeServerSetting"]["LoggingConfigFile"]
setting=LoadJsonFile(FilePath) if PathConfirm(FilePath) else BASE_LOGGINF_SETTING
logging.config.dictConfig(setting)
ExchangeServerLogger=logging.getLogger("ExchangeServerLogger")
ClientLogger=logging.getLogger("ClientLogger")
GuiLogger=logging.getLogger("GuiLogger")

################################################ ������ #################################################################
if __name__ =='__main__':
    print(PathConfirm("..\PyMod"))
    # ExchangeServerLogger.Debug("XXX")
    # ExchangeServerLogger.Warn("XXX")
    # ExchangeServerLogger.Error("XXX")
