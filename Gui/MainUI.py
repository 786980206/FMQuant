# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(731, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MainTab = QtWidgets.QTabWidget(self.centralwidget)
        self.MainTab.setObjectName("MainTab")
        self.Tab_Operate = QtWidgets.QWidget()
        self.Tab_Operate.setObjectName("Tab_Operate")
        self.gridLayout = QtWidgets.QGridLayout(self.Tab_Operate)
        self.gridLayout.setObjectName("gridLayout")
        self.GB_CancelOrder = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_CancelOrder.setObjectName("GB_CancelOrder")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.GB_CancelOrder)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.Label_6 = QtWidgets.QLabel(self.GB_CancelOrder)
        self.Label_6.setObjectName("Label_6")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_6)
        self.CB_CancelOrder_IDChose = QtWidgets.QComboBox(self.GB_CancelOrder)
        self.CB_CancelOrder_IDChose.setObjectName("CB_CancelOrder_IDChose")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.CB_CancelOrder_IDChose)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.pushButton = QtWidgets.QPushButton(self.GB_CancelOrder)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.gridLayout.addWidget(self.GB_CancelOrder, 1, 0, 2, 1)
        self.GB_PlaceOrder = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_PlaceOrder.setObjectName("GB_PlaceOrder")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.GB_PlaceOrder)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.GB_PlaceOrder)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.GB_PlaceOrder)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(self.GB_PlaceOrder)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.CB_PlaceOrder_Code = QtWidgets.QLineEdit(self.GB_PlaceOrder)
        self.CB_PlaceOrder_Code.setObjectName("CB_PlaceOrder_Code")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.CB_PlaceOrder_Code)
        self.Label_2 = QtWidgets.QLabel(self.GB_PlaceOrder)
        self.Label_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.CB_PlaceOrder_Direction = QtWidgets.QComboBox(self.GB_PlaceOrder)
        self.CB_PlaceOrder_Direction.setObjectName("CB_PlaceOrder_Direction")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.CB_PlaceOrder_Direction)
        self.Label_4 = QtWidgets.QLabel(self.GB_PlaceOrder)
        self.Label_4.setObjectName("Label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_4)
        self.CB_PlaceOrder_Price = QtWidgets.QLineEdit(self.GB_PlaceOrder)
        self.CB_PlaceOrder_Price.setObjectName("CB_PlaceOrder_Price")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.CB_PlaceOrder_Price)
        self.Label_3 = QtWidgets.QLabel(self.GB_PlaceOrder)
        self.Label_3.setObjectName("Label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_3)
        self.CB_PlaceOrder_Volume = QtWidgets.QLineEdit(self.GB_PlaceOrder)
        self.CB_PlaceOrder_Volume.setObjectName("CB_PlaceOrder_Volume")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.CB_PlaceOrder_Volume)
        self.Label_5 = QtWidgets.QLabel(self.GB_PlaceOrder)
        self.Label_5.setObjectName("Label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Label_5)
        self.CB_PlaceOrder_AddPar = QtWidgets.QLineEdit(self.GB_PlaceOrder)
        self.CB_PlaceOrder_AddPar.setObjectName("CB_PlaceOrder_AddPar")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.CB_PlaceOrder_AddPar)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.GB_PlaceOrder, 0, 0, 1, 1)
        self.GB_Quote = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_Quote.setObjectName("GB_Quote")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GB_Quote)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.Label_7 = QtWidgets.QLabel(self.GB_Quote)
        self.Label_7.setObjectName("Label_7")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_7)
        self.LB_Code = QtWidgets.QLabel(self.GB_Quote)
        self.LB_Code.setObjectName("LB_Code")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LB_Code)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.GB_Quote)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(self.GB_Quote)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.Label_8 = QtWidgets.QLabel(self.GB_Quote)
        self.Label_8.setObjectName("Label_8")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_8)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LB_SP1 = QtWidgets.QLabel(self.GB_Quote)
        self.LB_SP1.setObjectName("LB_SP1")
        self.horizontalLayout.addWidget(self.LB_SP1)
        self.LB_SV1 = QtWidgets.QLabel(self.GB_Quote)
        self.LB_SV1.setObjectName("LB_SV1")
        self.horizontalLayout.addWidget(self.LB_SV1)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.Label_9 = QtWidgets.QLabel(self.GB_Quote)
        self.Label_9.setObjectName("Label_9")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_9)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LB_BP1 = QtWidgets.QLabel(self.GB_Quote)
        self.LB_BP1.setObjectName("LB_BP1")
        self.horizontalLayout_2.addWidget(self.LB_BP1)
        self.LB_BV1 = QtWidgets.QLabel(self.GB_Quote)
        self.LB_BV1.setObjectName("LB_BV1")
        self.horizontalLayout_2.addWidget(self.LB_BV1)
        self.formLayout_2.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.formLayout_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.GB_Quote, 0, 1, 3, 1)
        self.GB_Position = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_Position.setObjectName("GB_Position")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.GB_Position)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.TV_Position = QtWidgets.QTableView(self.GB_Position)
        self.TV_Position.setObjectName("TV_Position")
        self.verticalLayout_9.addWidget(self.TV_Position)
        self.gridLayout.addWidget(self.GB_Position, 4, 0, 1, 3)
        self.GB_OrderList = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_OrderList.setObjectName("GB_OrderList")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.GB_OrderList)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.TV_OrderList = QtWidgets.QTableView(self.GB_OrderList)
        self.TV_OrderList.setObjectName("TV_OrderList")
        self.verticalLayout_6.addWidget(self.TV_OrderList)
        self.gridLayout.addWidget(self.GB_OrderList, 3, 0, 1, 3)
        self.GB_Log = QtWidgets.QGroupBox(self.Tab_Operate)
        self.GB_Log.setObjectName("GB_Log")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.GB_Log)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.LV_LogList = QtWidgets.QListView(self.GB_Log)
        self.LV_LogList.setObjectName("LV_LogList")
        self.verticalLayout_5.addWidget(self.LV_LogList)
        self.gridLayout.addWidget(self.GB_Log, 0, 2, 3, 1)
        self.MainTab.addTab(self.Tab_Operate, "")
        self.Tab_Order = QtWidgets.QWidget()
        self.Tab_Order.setObjectName("Tab_Order")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Tab_Order)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.TabOrderLO = QtWidgets.QVBoxLayout()
        self.TabOrderLO.setContentsMargins(1, 1, 1, 1)
        self.TabOrderLO.setSpacing(1)
        self.TabOrderLO.setObjectName("TabOrderLO")
        self.TV_OrderList_Main = QtWidgets.QTableView(self.Tab_Order)
        self.TV_OrderList_Main.setFrameShape(QtWidgets.QFrame.Box)
        self.TV_OrderList_Main.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TV_OrderList_Main.setObjectName("TV_OrderList_Main")
        self.TabOrderLO.addWidget(self.TV_OrderList_Main)
        self.verticalLayout_4.addLayout(self.TabOrderLO)
        self.MainTab.addTab(self.Tab_Order, "")
        self.Tab_Position = QtWidgets.QWidget()
        self.Tab_Position.setObjectName("Tab_Position")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.Tab_Position)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TabPositionLO = QtWidgets.QVBoxLayout()
        self.TabPositionLO.setContentsMargins(1, 1, 1, 1)
        self.TabPositionLO.setSpacing(1)
        self.TabPositionLO.setObjectName("TabPositionLO")
        self.TV_Position_Main = QtWidgets.QTableView(self.Tab_Position)
        self.TV_Position_Main.setFrameShape(QtWidgets.QFrame.Box)
        self.TV_Position_Main.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TV_Position_Main.setObjectName("TV_Position_Main")
        self.TabPositionLO.addWidget(self.TV_Position_Main)
        self.verticalLayout_8.addLayout(self.TabPositionLO)
        self.MainTab.addTab(self.Tab_Position, "")
        self.Tab_Transaction = QtWidgets.QWidget()
        self.Tab_Transaction.setObjectName("Tab_Transaction")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.Tab_Transaction)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.TabTransactionLO = QtWidgets.QVBoxLayout()
        self.TabTransactionLO.setContentsMargins(1, 1, 1, 1)
        self.TabTransactionLO.setSpacing(1)
        self.TabTransactionLO.setObjectName("TabTransactionLO")
        self.TV_Transaction_Main = QtWidgets.QTableView(self.Tab_Transaction)
        self.TV_Transaction_Main.setFrameShape(QtWidgets.QFrame.Box)
        self.TV_Transaction_Main.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TV_Transaction_Main.setObjectName("TV_Transaction_Main")
        self.TabTransactionLO.addWidget(self.TV_Transaction_Main)
        self.verticalLayout_7.addLayout(self.TabTransactionLO)
        self.MainTab.addTab(self.Tab_Transaction, "")
        self.verticalLayout.addWidget(self.MainTab)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 731, 23))
        self.menubar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menubar.setObjectName("menubar")
        self.Menu_Sys = QtWidgets.QMenu(self.menubar)
        self.Menu_Sys.setObjectName("Menu_Sys")
        self.Menu_Common = QtWidgets.QMenu(self.menubar)
        self.Menu_Common.setObjectName("Menu_Common")
        self.Menu_LogIn = QtWidgets.QMenu(self.menubar)
        self.Menu_LogIn.setObjectName("Menu_LogIn")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Menu_Setting = QtWidgets.QAction(MainWindow)
        self.Menu_Setting.setObjectName("Menu_Setting")
        self.Menu_LogIn_Action = QtWidgets.QAction(MainWindow)
        self.Menu_LogIn_Action.setObjectName("Menu_LogIn_Action")
        self.Menu_Sys.addAction(self.Menu_Setting)
        self.Menu_LogIn.addAction(self.Menu_LogIn_Action)
        self.menubar.addAction(self.Menu_Sys.menuAction())
        self.menubar.addAction(self.Menu_Common.menuAction())
        self.menubar.addAction(self.Menu_LogIn.menuAction())

        self.retranslateUi(MainWindow)
        self.MainTab.setCurrentIndex(0)
        self.Menu_LogIn_Action.triggered.connect(self.statusbar.clearMessage)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.GB_CancelOrder.setTitle(_translate("MainWindow", "撤单"))
        self.Label_6.setText(_translate("MainWindow", "订单编号"))
        self.pushButton.setText(_translate("MainWindow", "撤单"))
        self.GB_PlaceOrder.setTitle(_translate("MainWindow", "买卖"))
        self.pushButton_2.setText(_translate("MainWindow", "下单"))
        self.pushButton_3.setText(_translate("MainWindow", "重置"))
        self.Label.setText(_translate("MainWindow", "代码："))
        self.Label_2.setText(_translate("MainWindow", "方向："))
        self.Label_4.setText(_translate("MainWindow", "价格："))
        self.Label_3.setText(_translate("MainWindow", "数量："))
        self.Label_5.setText(_translate("MainWindow", "其他："))
        self.GB_Quote.setTitle(_translate("MainWindow", "行情"))
        self.Label_7.setText(_translate("MainWindow", "代码："))
        self.LB_Code.setText(_translate("MainWindow", "000001.SZSE"))
        self.label_8.setText(_translate("MainWindow", "价格"))
        self.label_7.setText(_translate("MainWindow", "数量"))
        self.Label_8.setText(_translate("MainWindow", "卖一："))
        self.LB_SP1.setText(_translate("MainWindow", "10.00"))
        self.LB_SV1.setText(_translate("MainWindow", "1000"))
        self.Label_9.setText(_translate("MainWindow", "买一："))
        self.LB_BP1.setText(_translate("MainWindow", "9.95"))
        self.LB_BV1.setText(_translate("MainWindow", "800"))
        self.GB_Position.setTitle(_translate("MainWindow", "持仓"))
        self.GB_OrderList.setTitle(_translate("MainWindow", "委托"))
        self.GB_Log.setTitle(_translate("MainWindow", "日志"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Tab_Operate), _translate("MainWindow", "下单"))
        self.Tab_Order.setToolTip(_translate("MainWindow", "<html><head/><body><p>Test</p></body></html>"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Tab_Order), _translate("MainWindow", "委托"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Tab_Position), _translate("MainWindow", "持仓"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Tab_Transaction), _translate("MainWindow", "成交"))
        self.Menu_Sys.setTitle(_translate("MainWindow", " 系统"))
        self.Menu_Common.setTitle(_translate("MainWindow", "常用"))
        self.Menu_LogIn.setTitle(_translate("MainWindow", "登录"))
        self.Menu_Setting.setText(_translate("MainWindow", "设置"))
        self.Menu_LogIn_Action.setText(_translate("MainWindow", "登录"))

