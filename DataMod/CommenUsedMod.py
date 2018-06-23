#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WindSing'
####################################### 一些说明 #######################################################################

####################################### 导入模块 #######################################################################
import sys
import time
import codecs
import DataModify
import DataDef
import re
####################################### 常量定义 #######################################################################
####################################### 函数定义 #######################################################################
# 读取文件
def ReadFile(FilePath,encoding='utf-8'):
	TempFile=open(FilePath,'r',encoding=encoding)
	FileContent=TempFile.read()
	TempFile.close()
	return FileContent
# 写文件
def WriteFile(AimStr,FilePath,Mod='w',encoding='utf-8'):
	TempFile=open(FilePath,Mod,encoding=encoding)
	TempFile.write(AimStr)
	TempFile.close()
# 检查并返回合法文件名
def checkNameValid(name=None):
    """
    检测Windows文件名称！
    """
    if name is None:
        print("name is None!")
        return
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid_name = reg.findall(name)
    if valid_name:
        for nv in valid_name:
            name = name.replace(nv, "_")
    return name