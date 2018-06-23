# -*- coding: UTF-8 -*-

import os,sys
script_path = os.path.realpath(__file__)
work_path = os.path.dirname(script_path)
#del os.environ["TMPPYTHONPATH"]
sys.path.append(work_path)
# import QtPyAPI
#print (QtPyAPI.__file__)
# os.chdir(work_path)
#print QtPyAPI.__file__
#********* QtAPI登录，启动API环境 *************
#param qtUser Qt用户
#param qtPwd Qt用户密码
#param option 预留参数，逗号分割的键值对序列
#ret 0 成功 >0 错误
def QtLogin(qtUser,qtPwd,options = ""):
    strLogin = QtPyAPI.string()
    ret = QtPyAPI.QtLogin(strLogin, qtUser, qtPwd, options)
    return ret, strLogin.c_str()
    
#************ QtAPI登出，停止API环境  *************
#note  QtAPI登出必须使用原QtAPI登录用户进行。
#param gtaUsr 国泰安用户
#ret 0 成功  >0 错误 
def QtLogout(qtUser):
    errorMsg = QtPyAPI.string()
    ret = QtPyAPI.QtLogout(errorMsg, qtUser)
    return ret, errorMsg.c_str()

if __name__=='__main__':
    pass


