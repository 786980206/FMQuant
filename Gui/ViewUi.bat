@echo off
title Client(FMQuant)
:: ��������·��ΪJupyter·�����ɣ�Python�汾λ3.5.2
echo ���������л���(��1,�칫2)��
set/p key=
if %key%==1 goto a
if %key%==2 goto b
goto c
:a
echo ���ڿ���Client(FMQuant)
E:\Miniconda35\Scripts\pyuic5.exe MainUI.ui -o MainUI.py
E:\Miniconda35\Scripts\pyuic5.exe WD_Login.ui -o WD_Login.py
E:\Miniconda35\python.exe E:/GitProj/FMQuant/Gui/Main.py
:b
echo ���ڿ���Client(FMQuant)
D:\Miniconda-Py3.5.2\Scripts\pyuic5.exe MainUI.ui -o MainUI.py
D:\Miniconda-Py3.5.2\Scripts\pyuic5.exe WD_Login.ui -o WD_Login.py
D:\Miniconda-Py3.5.2\python.exe E:/GitProj/FMQuant/Gui/Main.py
:c
echo ��������˳���
pause >nul
