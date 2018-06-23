#coding=gbk
__author__ = 'WindSing'

################################################# ģ�鵼�� ##############################################################
import logging
import logging.config
from configobj import ConfigObj
from validate import Validator
import ctypes
FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
STD_OUTPUT_HANDLE= -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

################################################ �������� ###############################################################
#  ����
LOG_CONFIG_PATH='..\\Setting\\Log.ini'

################################################ �������� ###############################################################
# ���������ļ��ĺ���-----------------------------------------------------------------
def LoadIni(FilePath,ConfigSpecPath=None):
    config = ConfigObj(FilePath,configspec=ConfigSpecPath)
    validator = Validator()
    if ConfigSpecPath!=None:
        result = config.validate(validator)
    return config
# ��־��ʾ����������ͨ��������ʵ����־�����ʽ�ı仯-------------------------------
def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
# ��־��ʼ����
def Log(AtFirst=False):
    if AtFirst:
        logging.config.fileConfig(LOG_CONFIG_PATH)
        # logging.config.fileConfig(r"E:\OneDrive\0_Coding\010_MyQuantSystem\Beta5.0\Setting\Log.ini")
    return logging.getLogger("PyMod")
def LogWithColor(Msg,Func,Color):
    set_color(Color)
    Func(Msg)
    set_color(FOREGROUND_WHITE)

################################################ ������ #################################################################
if __name__ =='__main__':
    pass