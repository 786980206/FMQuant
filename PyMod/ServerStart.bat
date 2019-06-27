@echo off
title ExchangeServer(FMQuant)
:: 更改下面路径为Jupyter路径即可，Python版本位3.5.2
echo 请输入运行环境(家1,办公2)：
set/p key=
if %key%==1 goto a
if %key%==2 goto b
goto c
:a
echo 正在开启ExchangeServer
E:\Miniconda35\python.exe E:/GitProj/FMQuant/PyMod/ExchangeServer.py
:b
echo 正在开启ExchangeServer
D:\Miniconda-Py3.5.2\python.exe E:/GitProj/FMQuant/PyMod/ExchangeServer.py
:c
echo 按任意键退出。
pause >nul
