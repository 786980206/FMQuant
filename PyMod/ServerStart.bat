@echo off
title ExchangeServer(FMQuant)
:: ��������·��ΪJupyter·�����ɣ�Python�汾λ3.5.2
echo ���������л���(��1,�칫2)��
set/p key=
if %key%==1 goto a
if %key%==2 goto b
goto c
:a
echo ���ڿ���ExchangeServer
E:\Miniconda35\python.exe E:/GitProj/FMQuant/PyMod/ExchangeServer.py
:b
echo ���ڿ���ExchangeServer
D:\Miniconda-Py3.5.2\python.exe E:/GitProj/FMQuant/PyMod/ExchangeServer.py
:c
echo ��������˳���
pause >nul
