# -*- coding: utf-8 -*-

import sys,time,threading
sys.path.append("..")
sys.path.append("../PyMod")
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import GeneralMod

import MainUI,WD_LogIn
from PyMod import Counter,Market

Lock=threading.Lock()
MainWindow=None

# 主窗口类
class FMQMainWindow(QMainWindow):
    def __init__(self,ui):
        super().__init__()
        self.ui=ui
        self.initUI()
    # 初始化界面
    def initUI(self):
        self.ui.setupUi(self)
        self.statusBar().showMessage("初始化...")
        self.show()

# 对话窗口基类
class FMQDialogLogin(QDialog):
    def __init__(self,ui,ParentWindow,ClientAppSetting):
        super().__init__()
        self.ParentWindow=ParentWindow
        self.ui = ui
        self.ClientAppSetting=ClientAppSetting
        self.initUI()
    # 初始化界面
    def initUI(self):
        self.ui.setupUi(self)
        # 设置模式为模态
        self.setWindowModality(Qt.ApplicationModal)
        # 加载数据
        self.LoadSetting()
        # 展示
        self.show()

    # 加载配置
    def LoadSetting(self):
        self.ui.WD_LogIn_Usr.setText(str(self.ClientAppSetting["Usr"]))
        self.ui.WD_LogIn_Pwd.setText(str(self.ClientAppSetting["Pwd"]))
        self.ui.WD_Login_ExchangeServerHost.setText(str(self.ClientAppSetting["AddPar"]["ExchangeServerHost"]))
        self.ui.WD_Login_ExchangeServerPort.setText(str(self.ClientAppSetting["AddPar"]["ExchangeServerPort"]))
        self.ui.WD_Mkt_MktServerHost.setText(str(self.ClientAppSetting["Mkt"]["MktServerHost"]))
        self.ui.WD_Mkt_MktServerPort.setText(str(self.ClientAppSetting["Mkt"]["MktServerPort"]))
        self.ui.WD_LogIn_MaxConnnectTryTime.setText(str(self.ClientAppSetting["AddPar"]["MaxConnnectTryTime"]))
        self.ui.WD_LogIn_WaitTimeAfterTryConnect.setText(str(self.ClientAppSetting["AddPar"]["WaitTimeAfterTryConnect"]))
        self.ui.WD_LogIn_CounterType.setText(str(self.ClientAppSetting["CounterType"]))
        self.ui.WD_Login_CommissionRate.setText(str(self.ClientAppSetting["CommissionRate"]))

    # 保存配置
    def SaveSetting(self):
        self.ClientAppSetting["Usr"]=self.ui.WD_LogIn_Usr.text()
        self.ClientAppSetting["Pwd"]=self.ui.WD_LogIn_Pwd.text()
        self.ClientAppSetting["AddPar"]["ExchangeServerHost"]=self.ui.WD_Login_ExchangeServerHost.text()
        self.ClientAppSetting["AddPar"]["ExchangeServerPort"]=int(self.ui.WD_Login_ExchangeServerPort.text())
        self.ClientAppSetting["Mkt"]["MktServerHost"]=self.ui.WD_Mkt_MktServerHost.text()
        self.ClientAppSetting["Mkt"]["MktServerPort"]=int(self.ui.WD_Mkt_MktServerPort.text())
        self.ClientAppSetting["AddPar"]["MaxConnnectTryTime"]=int(self.ui.WD_LogIn_MaxConnnectTryTime.text())
        self.ClientAppSetting["AddPar"]["WaitTimeAfterTryConnect"]=int(self.ui.WD_LogIn_WaitTimeAfterTryConnect.text())
        self.ClientAppSetting["CounterType"]=self.ui.WD_LogIn_CounterType.text()
        self.ClientAppSetting["CommissionRate"]=float(self.ui.WD_Login_CommissionRate.text())
        self.WriteSettingFile()

    # 写配置文件
    def WriteSettingFile(self):
        GeneralMod.SaveJsonFile("../Setting/ClientAppSetting.json",self.ClientAppSetting)

    # 登录事件
    def LogIn(self):
        # 保存配置
        self.SaveSetting()
        # 当前窗口消失
        self.hide()
        # 初始化连接对象
        Mkt = Market.MktSliNow()
        Account=Counter.Account(self.ClientAppSetting["Usr"],self.ClientAppSetting["Pwd"],self.ClientAppSetting["AddPar"],MktSliNow=Mkt,ClientGui=self.ParentWindow)
        # 等待连接
        while Account.LogInState == 0:
            self.ParentWindow.statusBar().showMessage("登录中...")
            time.sleep(1)
        # 连接成功
        self.ParentWindow.statusBar().showMessage("已登录")



def GuiInit():
    app = QApplication(sys.argv)
    MainWindow = FMQMainWindow()
    return app,MainWindow


def CounterInit():
    # 设置涨跌停价格等市场信息
    Mkt = Market.MktSliNow()
    AddPar = {
        "ExchangeServerHost": "127.0.0.1",
        "ExchangeServerPort": 9501,
        "MaxConnnectTryTime": 100,
        "WaitTimeAfterTryConnect": 2
    }
    Account = Counter.Account('usr', 'pwd', AddPar, MktSliNow=Mkt)
    while Account.LogInState != 1:
        print("等待登录中！")
        time.sleep(2)
    Init(Mkt,Account)

def Init(Mkt, Account):
    Mkt.Data['Price_LimitUp'] = 15
    Mkt.Data['Price_LimitDown'] = 5
    Mkt.Data['Price'] = 10
    Mkt.Data['Volume4Trd'] = 200
    # 设置账户信息
    Account.AccPar['CommissionRate'] = 0.01
    Account.AccPar['Slippage'] = 0.1
    Account.CashInfo = {'Cash': 10000, 'CashF': 0, 'InitCash': 10000, 'CashA': 10000}
    Account.Position['000001.SZSE'] = ['000001.SZSE', 1200, 600, 600, 0, 0, 'PriceNow', 0, 0, 0, 'CNY', 'Mkt',
                                       Account, {}]


if __name__ == '__main__':
    ClientAppSetting=GeneralMod.LoadJsonFile(GeneralMod.PathJoin("../Setting/ClientAppSetting.json"))
    # 启动GUI
    # app,MainWindow=GuiInit()
    # 启动主窗口
    MainApp = QApplication(sys.argv)
    MainWindow = FMQMainWindow(MainUI.Ui_MainWindow())
    # 初始化登录对话框
    LogInWD=FMQDialogLogin(WD_LogIn.Ui_WD_LogIn(),MainWindow,ClientAppSetting)
    # 连接主窗口登录菜单按钮事件
    MainWindow.ui.Menu_LogIn_Action.triggered.connect(LogInWD.show)
    LogInWD.ui.BT_LogIn.clicked.connect(LogInWD.LogIn)

    MainWindow.statusBar().showMessage("未连接")
    sys.exit(MainApp.exec_())
