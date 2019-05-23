# -*- coding: UTF-8 -*-

import os,sys
# print(sys.path)
import QtPyAPI

#********* QtAPI登录，启动API环境 *************
#param qtUser Qt用户
#param qtPwd Qt用户密码
#param option 预留参数，逗号分割的键值对序列
#ret 0 成功 >0 错误
def QtLogin(qtUser,qtPwd,options = ""):
    os.chdir('lib')
    strLogin = QtPyAPI.string()
    ret = QtPyAPI.QtLogin(strLogin, qtUser, qtPwd, options)
    os.chdir('..')
    return ret, strLogin.c_str()
    
#************ QtAPI登出，停止API环境  *************
#note  QtAPI登出必须使用原QtAPI登录用户进行。
#param gtaUsr 国泰安用户
#ret 0 成功  >0 错误 
def QtLogout(qtUser):
    os.chdir('lib')
    errorMsg = QtPyAPI.string()
    ret = QtPyAPI.QtLogout(errorMsg, qtUser)
    os.chdir('..')
    return ret, errorMsg.c_str()

if __name__=='__main__':
    pass


