# -*- coding: utf-8 -*-

import sys,time,threading
sys.path.append("..")
sys.path.append("../PyMod")
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import GeneralMod
from multiprocessing import Process,Queue
import datetime

import MainUI,WD_LogIn
from PyMod import Counter,Market
from GeneralMod import GuiLogger

Lock=threading.Lock()
MainWindow=None

# 主窗口类
class FMQMainWindow(QMainWindow):
    def __init__(self,ui,ClientAppSetting):
        super().__init__()
        # 初始化数据
        # 初始化ui
        self.ui = ui
        self.initUI()
        # 其他数据
        self.ClientAppSetting = ClientAppSetting
        self.LogInWD=FMQDialogLogin(WD_LogIn.Ui_WD_LogIn(),self,self.ClientAppSetting)
        self.BackgroundServerThread=None
        self.ListenFromBackgroundServerThread=None
        self.Account=None
        self.LogInState=0
        # 绑定事件
        self.SetConnect()
        # 绑定Queue
        self.GetQueue=Queue()
        self.PutQueue=Queue()

    # 初始化界面
    def initUI(self):
        self.ui.setupUi(self)
        # 设置状态栏
        self.RefreashStatusBarMsg("初始化...")
        self.StatusBarItem=[QLabel(),QLabel(),QLabel(),QLabel(),QLabel()]
        self.RefleshStatePresent("未登录","未连接")
        [self.statusBar().addPermanentWidget(x) for x in self.StatusBarItem]
        self.show()
        # 设置持仓列表
        self.ui.TV_PositionList.setColumnCount(13)
        self.ui.TV_PositionList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.TV_PositionList.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        self.ui.TV_PositionList.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        self.ui.TV_PositionList.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置只有行选中
        self.ui.TV_PositionList.setHorizontalHeaderLabels(["证券代码","持仓量","可用量","冻结量","股票实际","成本价","市价","市值","浮动盈亏","盈亏比例","币种","交易市场","附加参数"])
        # 设置委托列表
        self.ui.TV_OrderList.setColumnCount(11)
        self.ui.TV_OrderList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.TV_OrderList.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        self.ui.TV_OrderList.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        self.ui.TV_OrderList.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置只有行选中
        self.ui.TV_OrderList.setHorizontalHeaderLabels(["证券代码","方向","委托价格","委托数量","成交数量","订单状态","成交均价","委托时间","订单编号","交易市场","附加参数"])
        # 设置订单方向
        self.ui.CB_PlaceOrder_Direction.addItems(["买入","卖出"])
        # 设置输入校验
        self.ui.CB_PlaceOrder_Price.setValidator(QDoubleValidator())
        self.ui.CB_PlaceOrder_Volume.setValidator(QIntValidator())


    # 更新界面账户状态显示
    def RefleshStatePresent(self, Usr,State):
        self.StatusBarItem[3].setText(str(Usr))
        self.StatusBarItem[4].setText(str(State))

    # 绑定事件
    def SetConnect(self):
        # 登录菜单按钮
        self.ui.Menu_LogIn_Action.triggered.connect(self.LogInWD.show)
        # 登出菜单按钮
        self.ui.Menu_LogOut_Action.triggered.connect(self.OnLogOut)
        # 下单按钮
        self.ui.BT_PlaceOrder.clicked.connect(self.PlaceOrder)
        # 撤单按钮
        self.ui.BT_CancelOrder.clicked.connect(self.CancelOrder)

        # self.ui.Menu_Setting.triggered.connect(self.Reset)

    # 处理从后台服务接收的消息
    def DealMsgFromBST(self,Msg):
        try:
            GuiLogger.debug("GUI开始处理消息:{}".format(Msg))
            self.RefreashLogList(Msg)
            if Msg["MsgType"]=="LogInReturn":
                self.OnLogInReturn(Msg)
            elif Msg["MsgType"]=="Disconnect":
                self.LogInState = 0
                self.RefreashStatusBarMsg("连接断开...")
            elif Msg["MsgType"]=="Reconnect":
                self.RefreashStatusBarMsg("重连中...")
            elif Msg["MsgType"]=="LogOut":
                self.OnLogOut(Msg)
            elif Msg["MsgType"]=="RetOrderList":
                self.RefreshOrder(Msg["Order"])
            elif Msg["MsgType"]=="RetPositionList":
                self.RefreshPosition(Msg["Position"])
            elif Msg["MsgType"]=="RetCashInfo":
                self.RefreshCashInfo(Msg["CashInfo"])
            elif Msg["MsgType"]=="RetCheckOrder":
                self.OnCheckOrderReturn(Msg["ret"],Msg["msg"])
        except Exception as e:
            GuiLogger.error(e)

    # 向LogList添加消息
    def RefreashLogList(self,Msg,Mod="add"):
        if Mod=="add":
            self.ui.LV_LogList.addItem("[{}]    {}".format(datetime.datetime.now(),str(Msg)))

    # 登录消息回执
    def OnLogInReturn(self,Msg):
        if Msg["ret"]==1:
            # 登录成功
            self.RefreashStatusBarMsg("已登录")
            self.RefleshStatePresent(self.ClientAppSetting["Usr"],"已连接")
            # self.RefleshCashPresent(100000, 80000,20000)
            self.GetAccountInfo()
            self.LogInState=1
        else:
            self.LogInWD.ui.BT_LogIn.setEnabled(True)
            self.RefreashStatusBarMsg("登录失败")
            self.LogInState = 0

    # 登出消息回执
    def OnLogOut(self, Msg):
        # 更新界面元素
        self.LogInWD.ui.BT_LogIn.setEnabled(True)
        self.RefreashStatusBarMsg("未连接")
        self.RefleshStatePresent("未登录","未连接")
        self.RefreshCashInfo(["","",""])
        self.RefreshOrder([])
        self.RefreshPosition([])
        # 清理进程资源
        self.BackgroundServerThread=None
        self.ListenFromBackgroundServerThread=None
        self.Account = None
        # 更新状态
        self.LogInState = 0

    # 订单检验回执
    def OnCheckOrderReturn(self,ret,msg):
        if ret==0:
            QMessageBox.information(self, "提示","下单失败：{}".format(msg),QMessageBox.Yes)

    # 更新状态栏消息
    def RefreashStatusBarMsg(self,Msg,sec=0):
        self.statusBar().showMessage(str(Msg),sec)

    # 向后台进程发送消息
    def SendMsgToBST(self,Msg):
        self.PutQueue.put(Msg)

    # 获取账户信息
    def GetAccountInfo(self):
        Msg={"MsgType":"GetAccountInfo"}
        self.SendMsgToBST(Msg)

    # 更新持仓列表
    def RefreshPosition(self,PositionList):
        self.ui.TV_PositionList.setRowCount(len(PositionList))  # 行数
        for i in range(len(PositionList)):  # 注意上面列表中数字加单引号，否则下面不显示(或者下面str方法转化一下即可)
            item = PositionList[i]
            for j in range(len(item)):
                item = QTableWidgetItem(str(PositionList[i][j]))
                self.ui.TV_PositionList.setItem(i, j, item)

    # 更新委托列表
    def RefreshOrder(self,OrderList):
        self.ui.CB_CancelOrder_IDChose.clear()
        self.ui.TV_OrderList.setRowCount(len(OrderList))  # 行数
        for i in range(len(OrderList)):  # 注意上面列表中数字加单引号，否则下面不显示(或者下面str方法转化一下即可)
            item = OrderList[i]
            self.ui.CB_CancelOrder_IDChose.addItem(OrderList[i][8])
            for j in range(len(item)):
                item = QTableWidgetItem(str(OrderList[i][j]))
                self.ui.TV_OrderList.setItem(i, j, item)

    #  更新资金状态
    def RefreshCashInfo(self,CashInfo):
        self.StatusBarItem[0].setText(str(CashInfo[0]))
        self.StatusBarItem[1].setText(str(CashInfo[1]))
        self.StatusBarItem[2].setText(str(CashInfo[2]))

    # 下单函数
    def PlaceOrder(self):
        if self.LogInState==1:
            Msg={"MsgType":"PlaceOrder"}
            Order=self.GetOrderPlaceInfo()
            Msg["Order"]=Order
            self.SendMsgToBST(Msg)
        else:
            QMessageBox.information(self, "提示","用户未登录！",QMessageBox.Yes)
        # self.SendMsgToBST(Msg)

    # 从界面获取下单信息
    def GetOrderPlaceInfo(self):
        try:
            Code=self.ui.CB_PlaceOrder_Code.text()
            Direction=self.ui.CB_PlaceOrder_Direction.currentText()
            if Direction=="买入":
                Direction=1
            elif Direction=="卖出":
                Direction=0
            Price = float(self.ui.CB_PlaceOrder_Price.text()) if self.ui.CB_PlaceOrder_Price.text()!="" else 0
            Volume = int(self.ui.CB_PlaceOrder_Volume.text()) if self.ui.CB_PlaceOrder_Volume.text()!="" else 0
            AddPar = dict(self.ui.CB_PlaceOrder_AddPar.text())
            Order=[Code,Direction,Price,Volume,AddPar]
            return Order
        except Exception as e:
            GuiLogger.error(e)
    # 撤单函数
    def CancelOrder(self):
        if self.LogInState==1:
            Msg={"MsgType":"CancelOrder"}
            OrderID=self.GetOrderCancelInfo()
            Msg["OrderID"]=OrderID
            self.SendMsgToBST(Msg)
        else:
            QMessageBox.information(self, "提示","用户未登录！",QMessageBox.Yes)

    # 从界面获取测单信息
    def GetOrderCancelInfo(self):
        try:
            OrderID=self.ui.CB_CancelOrder_IDChose.currentText()
            return str(OrderID)
        except Exception as e:
            QMessageBox.information(self, "提示",str(e),QMessageBox.Yes)

    # 测试方法，重置
    def Reset(self):
        pass

# 对话窗口基类
class FMQDialogLogin(QDialog):
    def __init__(self,ui,ParentWindow,ClientAppSetting):
        super(FMQDialogLogin,self).__init__()
        self.ui = ui
        self.ClientAppSetting = ClientAppSetting
        self.initUI()
        self.ParentWindow=ParentWindow
        self.SetConnect()

    # 初始化界面
    def initUI(self):
        self.ui.setupUi(self)
        # 设置模式为模态
        self.setWindowModality(Qt.ApplicationModal)
        # 加载数据
        self.LoadSetting()
        # 展示
        self.show()

    # 绑定事件
    def SetConnect(self):
        self.ui.BT_LogIn.clicked.connect(self.LogIn)


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
        try:
            # 保存配置
            self.SaveSetting()
            # 当前窗口消失
            self.hide()
            self.ui.BT_LogIn.setEnabled(False)
            # 等待连接
            self.ParentWindow.RefreashStatusBarMsg("登录中...")
            # 初始化连接对象
            Mkt = Market.MktSliNow()
            Account=Counter.Account(self.ClientAppSetting["Usr"],self.ClientAppSetting["Pwd"],self.ClientAppSetting["AddPar"],MktSliNow=Mkt,ClientPutQueue=self.ParentWindow.GetQueue,ClientGetQueue=self.ParentWindow.PutQueue)
            self.Account=Account
            Init(Mkt,Account)
            BackgroundServerThread=Process(target=Account.ConnectAndLogin,args=(True,))
            self.ParentWindow.BackgroundServerThread = BackgroundServerThread
            # 开启消息监听线程
            # ListenFromBackgroundServerThread=threading.Thread(target=self.ParentWindow.ListenFromBST)
            ListenFromBackgroundServerThread=ListenThread(self.ParentWindow)
            self.ParentWindow.ListenFromBackgroundServerThread=ListenFromBackgroundServerThread
            # 绑定事件
            self.ParentWindow.ListenFromBackgroundServerThread.DealMsg.connect(self.ParentWindow.DealMsgFromBST)
            # 开启后台服务线程
            ListenFromBackgroundServerThread.start()
            BackgroundServerThread.start()
        except Exception as e:
            GuiLogger.error(e)

# 后台监听消息线程
class ListenThread(QThread):
    DealMsg=pyqtSignal(dict)

    def __init__(self,MainWindow):
        super(ListenThread, self).__init__()
        self.MainWindow=MainWindow

    def run(self):
        GuiLogger.debug("========================================监听BST========================================")
        if self.MainWindow.BackgroundServerThread!=None:
            while self.MainWindow.BackgroundServerThread!=None:
                try:
                    Msg=self.MainWindow.GetQueue.get()
                    # 通过信号槽发送到Gui
                    GuiLogger.debug("从Queue中收到消息:{}".format(Msg))
                    self.DealMsg.emit(Msg)
                except Exception as e:
                    GuiLogger.error(e)



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
        GuiLogger.debug("等待登录中！")
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
    Account.Position['000001.SZSE'] = ['000001.SZSE', 10000, 5000, 5000, 0, 10, '10', 0, 0, 0, 'CNY', 'Mkt',Account, {}]
    # Account.Order['AAA'] = ['000001.SZSE', 1, 0, 100, 0, "Wait2Matched", 0,"2019-04-19 17:00:00", "AAA",'Mkt',Account, {}]
    # Account.OrderRec['AAA'] = ['000001.SZSE', 1, 0, 100, 0, "Wait2Matched", 0, "2019-04-19 17:00:00", "AAA", 'Mkt',Account, {}]


if __name__ == '__main__':
    ClientAppSetting=GeneralMod.LoadJsonFile(GeneralMod.PathJoin("../Setting/ClientAppSetting.json"))
    # 启动GUI
    # app,MainWindow=GuiInit()
    # 启动主窗口
    MainApp = QApplication(sys.argv)
    MainWindow = FMQMainWindow(MainUI.Ui_MainWindow(),ClientAppSetting)

    MainWindow.RefreashStatusBarMsg("未连接")
    sys.exit(MainApp.exec_())
