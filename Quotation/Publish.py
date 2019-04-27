# -*- coding: utf-8 -*-

import socket
import multiprocessing
import threading
import datetime
import pandas as pd
import json
import time
import uuid
import Market
import GeneralMod
from GeneralMod import ExchangeServerLogger


def GetMsg(X):
	with open('SocketMsg.json') as f:
		Msg=json.load(f)
	return Msg[int(X)]


# ��������
POSITION_INDEX=['Code','Vol','VolA','VolFrozen','StockActualVol','AvgCost','PriceNow','MktValue','FloatingProfit','ProfitRatio','Currency','Mkt','Account','Config']
ORDER_INDEX=['Code','Direction','Price','Volume','VolumeMatched','State','AvgMatchingPrice','OrderTime','OrderNum','Mkt','Account','Config']
BUFFSIZE=1024 #������Ϣ��������С������Ժ󴫵���Ϣ���˻��޸�

# �ͻ���������
class ClientConnection(object):
	def __init__(self,conn,addr,ExchangeCore,ClientPool):
		self.addr=addr
		self.conn=conn
		self.ExchangeCore=ExchangeCore
		self.ClientID=str(uuid.uuid1())
		self.ClientPool=ClientPool
		self.AccountID=None
		ExchangeServerLogger.info("���ӳɹ�:{}".format(self.addr))
	# �˳�
	def Exit(self):
		self.conn.close()
		del self.ClientPool[self.ClientID]
		ExchangeServerLogger.info("���ӶϿ�:{}".format(self.addr))
		exit(0)
	# ������Ϣ
	def RecMsg(self):
		Lock=threading.Lock()
		Msg=''
		while True:
			try:
				RecData=self.conn.recv(BUFFSIZE).decode('utf-8')
				ExchangeServerLogger.debug("��ȡ����������:{}".format(RecData))
			except:
				ExchangeServerLogger.warning("���ջ���������ʧ��!")
				self.Exit()
			if RecData=='':self.Exit()
			Msglist,Msg=GeneralMod.AnalyzeMsg(Msg,RecData)
			for AimMsg in Msglist:
				try:
					Lock.acquire()
					self.DealRecMsg(AimMsg)
					Lock.release()
				except Exception as e:
					ExchangeServerLogger.error("������Ϣ����:{},{}".format(AimMsg,e))
	# ������Ϣ
	def SendMsg(self,Msg):
		Msg=GeneralMod.MakeSendMsg(Msg)
		self.conn.send(str(Msg).encode('utf-8'))
		ExchangeServerLogger.debug("�ɹ�������Ϣ:{}".format(Msg))
		return 1,"������Ϣ�ɹ�"

	# ���������Ϣ�ĺ���
	def DealRecMsg(self,Msg):
		ExchangeServerLogger.debug("������Ϣ:{}".format(Msg))
		# ���Դ�ӡ�ַ���
		if Msg['MsgType']=="Print":
			ExchangeServerLogger.debug('���������Ϣ���̴߳�ӡ��{}'.format(Msg))
		# �˳�
		if Msg['MsgType']=="Exit":
			self.Exit()
		# �¶�������
		if Msg['MsgType']=="PlaceOrder":
			OrderID,Order=Msg['OrderID'],Msg['Order']
			self.ExchangeCore.DealNewOrder(OrderID,Order,self)
		# ��������
		if Msg['MsgType']=="CancelOrder":
			OrderID=Msg['OrderID']
			self.ExchangeCore.CancelOrder(OrderID,self)
		# �˻���¼
		if Msg['MsgType']=="LogIn":
			self.CheckLogIn(Msg)
		# �˻��ǳ�
		if Msg['MsgType']=="LogOut":
			self.Exit()
		# ���������
		if Msg['MsgType']=="Clear":
			self.ExchangeCore.OrderPool=pd.DataFrame(index=ORDER_INDEX)
			ExchangeServerLogger.debug("���ExchangeCore.OrderPool�ɹ�")
	# ��¼���
	def CheckLogIn(self,Msg):
		ExchangeServerLogger.info("�ͻ��˵�¼:{}".format(Msg))
		if self.CheckUsr(Msg["Usr"],Msg["Pwd"]):
			self.AccountID=Msg['AccountID']
			Msg={'MsgType':'LogInReturn','ret':1,'msg':'��¼�ɹ�','session':'XXXXXXX'}
			ExchangeServerLogger.info("���͵�¼��ִ:{}".format(Msg))
			self.SendMsg(Msg)
	# �û���Ϣ���
	def CheckUsr(self,Usr,Pwd):
		ExchangeServerLogger.debug("��֤�û����:{},{}".format(Usr,Pwd))
		return 1


# ��ʼ��
def Init():
	ExchangeServerSetting=GeneralMod.LoadJsonFile(GeneralMod.PathJoin(GeneralMod.BASE_SETTING_FILE))["ExchangeServerSetting"]
	ExchangeCore=Exchange()
	ExchangeServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ExchangeServer.bind((ExchangeServerSetting["ExchangeServerHost"],ExchangeServerSetting["ExchangeServerPort"]))
	ExchangeServer.listen(ExchangeServerSetting["ExchangeServerListenLimit"])
	ClientPool={}
	ExchangeServerLogger.info("�����ɹ�:ExchangeServer")
	while True:
		ExchangeServerLogger.debug("�ȴ�������:ExchangeServer")
		conn,addr=ExchangeServer.accept()
		Client=ClientConnection(conn,addr,ExchangeCore,ClientPool)
		ClientPool[Client.ClientID]=Client
		# ClientThread=multiprocessing.Process(name="ClientThread({})".format(Client.ClientID),target=Client.RecMsg)
		ClientThread = threading.Thread(name="ClientThread({})".format(Client.ClientID), target=Client.RecMsg)
		# ���߳�Ϊ�ػ��߳�
		ClientThread.daemon=True
		ClientThread.start()
		ExchangeServerLogger.debug("�ͻ���({})�����ӣ���Ϣ�����߳������ɹ�".format(Client.ClientID))
		# # �ȴ��ͻ��˵�¼
		# time.sleep(ExchangeServerSetting["ClientLogInTimeLimit"])
		# # ���û����ָ��ʱ���ڵ�¼����ô�������ͻ�������
		# if Client.AccountID==None:Client.Exit()
		# ���ڵ���===============================================================
		# while 1:
		# 	# from SocketCliTest import GetMsg
		# 	time.sleep(1)
		# 	x = input(">>>").strip()
		# 	try:
		# 		if x[0] == 's' or x == 'S':
		# 			Msg = GetMsg(x[1])
		# 			# print(Msg)
		# 			ExchangeCore.SendMsg(Client,Msg)
		# 	except Exception as e:
		# 		print(e)
		# ���ڵ���===============================================================

################################################ �ඨ�� ###############################################################
class Exchange(object):
	# ��ʼ��
	def __init__(self,MktSliNow=None,OrderPool=None):
		self.OrderPool=OrderPool if OrderPool!=None else pd.DataFrame(index=ORDER_INDEX)
		self.MktSliNow=MktSliNow if MktSliNow!=None else Market.MktSliNow()
		self.Slippage=0

	# ��ͻ��˷�����Ϣ
	def SendMsg(self,Client,Msg):
		ExchangeServerLogger.debug("������Ϣ:{}".format(Msg))
		Client.SendMsg(Msg)

	# �����ر�
	def SendOrderReturn(self,OrderID,Client,ret,msg):
		if ret==1:
			OrderTime=self.OrderPool[OrderID][7]
		else:
			OrderTime=self.CreateOrderTime()
		Msg={
			'MsgType':'OrderReturn',
			'OrderID':OrderID,
			'ret':ret,
			'msg':msg,
			'OrderTime':OrderTime
		}
		ExchangeServerLogger.info("���ͱ�����ִ:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# �ɽ��ر�
	def SendTransactionReturn(self,OrderID,Client,MatchInfo,OrderState,MatchTime):
		Msg={
			'MsgType':'TransactionReturn',
			'OrderID':OrderID,
			'MatchInfo':MatchInfo,
			'OrderState':OrderState,
			'MatchTime':MatchTime
		}
		ExchangeServerLogger.info("���ͳɽ���ִ:{}".format(Msg))
		self.SendMsg(Client,Msg)

	# �����ر�
	def SendCancelOrderReturn(self,Client,OrderID,ret,msg,CancelTime):
		Msg={
			'MsgType':'CancelOrderReturn',
			'OrderID':OrderID,
			'ret':ret,
			'msg':msg,
			'CancelTime':CancelTime
		}
		ExchangeServerLogger.info("���ͳ�����ִ:{}".format(Msg))
		self.SendMsg(Client, Msg)

	# ��ȡ��������
	def GetOrderByID(self,OrderID,Item=ORDER_INDEX):
		if type(Item) is not list:Item=[Item]
		if OrderID in self.OrderPool.columns:
			return list(self.OrderPool[OrderID].loc[Item])
		else:
			return [None]*len(self.OrderPool.columns)

	# ���ɴ�ϳɽ�ʱ��
	def CreateMatchTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# ���ɳ���ʱ��
	def CreateCancelTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# �ж϶���״̬���綩��ȫ���ɽ�����Ҫȡ���ȣ�
	def CheckOrderByID(self,OrderID):
		ExchangeServerLogger.debug("��鶩��״̬:{}".format(OrderID))
		# ��������
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=self.GetOrderByID(OrderID)
		# �ж��Ƿ�ȫ���ɽ�
		if Volume==VolumeMatched and State=='AllMatched':
			# �������
			ret,msg=self.DelOrderByID(OrderID)
		else:
			ret,msg=1,"��������"
		return ret,msg

	# ɾ������
	def DelOrderByID(self,OrderID):
		ExchangeServerLogger.info("ɾ������:{}".format(OrderID))
		if OrderID not in self.OrderPool:
			return 0,'ɾ������ʧ�ܣ�����������'
		self.OrderPool.drop(labels=OrderID, axis=1, inplace=True)
		return 1,'ɾ�������ɹ�'

	# ���ɶ����µ�ʱ��
	def CreateOrderTime(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

	# ����¶���
	def CheckNewOrder(self,OrderID,Order,Client):
		ExchangeServerLogger.debug("����±���:{},{}".format(OrderID, Order))
		if OrderID in self.OrderPool:
			ret,msg=0, '���������ظ�'
			return ret,msg
		if Client.AccountID==None:
			return 0,'�˻�ID�쳣'
		ret,msg=self.LogNewOrder(OrderID,Order,Client)
		return ret,msg

	# ��¼�¶��������¶������붩����¼�в����ɶ���id
	def LogNewOrder(self,OrderID,Order,Client):
		ExchangeServerLogger.info("��¼�±���:{},{}".format(OrderID,Order))
		Code=Order['Code']
		Direction=Order['Direction']
		Price=Order['Price']
		Volume=Order['Volume']
		AddPar=Order['AddPar']
		# ��¼����
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,0,'WaitToMatch',0,self.CreateOrderTime(),OrderID,'Mkt',Client,AddPar]
		return 1,'�µ��ɹ�'

	# ����ӹ�̨���ƹ����Ķ�������
	def DealNewOrder(self,OrderID,Order,Client,MarkeSliNow=None):
		ExchangeServerLogger.info("�����±���:{},{}".format(OrderID,Order))
		# ����¶���
		ret,msg=self.CheckNewOrder(OrderID,Order,Client)
		ExchangeServerLogger.debug("��鱨�����:{},{}".format(ret,msg))
		# ���Ͷ����ر�
		self.SendOrderReturn(OrderID,Client,ret,msg)
		# ExchangeServerLogger.debug("���Ͷ����ر����:{},{}".format(ret, msg))
		# ��鲻ͨ�����˳�
		if ret==0:return
		# ��ʼ���
		ret,msg=self.MatchOrderByID(OrderID)
		return ret,msg

	# �����Ͻ��
	def DealMatchRetInOrderPool(self,OrderID,MatchInfo):
		ExchangeServerLogger.debug("OrderPool�����Ͻ��:{},{}".format(OrderID,MatchInfo))
		# ��������
		Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old=self.GetOrderByID(OrderID)
		# �ɽ�����
		PriceMatching=MatchInfo['PriceMatching']
		VolumeMatching=MatchInfo['VolumeMatching']
		# ��ʼ����
		# �����µĶ�����¼���ֶ�
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=Code_Old,Direction_Old,Price_Old,Volume_Old,VolumeMatched_Old,State_Old,AvgMatchingPrice_Old,OrderTime_Old,OrderNum_Old,Mkt_Old,Account_Old,Config_Old
		# �ѳɽ���
		VolumeMatched=VolumeMatched_Old+VolumeMatching
		# ״̬
		# ����ѳ�=������
		if VolumeMatched==Volume_Old:
			State='AllMatched'
		elif VolumeMatched<Volume_Old and VolumeMatched!=0:
			State='PartMatched'
		else:
			State='WaitToMatch'
		# ��д���ݵ�OrderPool
		self.OrderPool[OrderID]=[Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config]
		# ��鶩��״̬���綩��ȫ���ɽ�����Ҫɾ���ȣ�
		ret,msg=self.CheckOrderByID(OrderID)
		ExchangeServerLogger.debug("��鶩�����:{},{}".format(ret, msg))
		return 1,State

	# �����϶����ĺ���
	# ��Ҫ�õ��������ݣ��г����ݣ���̨���ݣ����ʵȣ�������������ݣ��绬�㣬���ɽ������ȣ�
	def MatchSimulation(self,OrderID,MktInfo):
		ExchangeServerLogger.debug("������:{},{}".format(OrderID,MktInfo))
		# ��������
		Code,Direction,Price,Volume,VolumeMatched,State,AvgMatchingPrice,OrderTime,OrderNum,Mkt,Account,Config=self.GetOrderByID(OrderID)
		# �г�����
		Price4Trd=MktInfo['Price4Trd']
		Volume4Trd=MktInfo['Volume4Trd']
		# �����������
		Slippage=self.Slippage
		# ���㶩��δ�ɽ���
		VolumeNotMatched=Volume-VolumeMatched
		# ��ʼ���
		# �۸�Ա�
		# �м۶൥
		if Price==0 and Direction==1:
			PriceMatching=Price4Trd+Slippage
		# �޼۶൥
		elif (Price>=Price4Trd) and Direction==1:
			PriceMatching=Price4Trd
		# �м�ƽ��
		elif Price==0 and Direction==0:
			PriceMatching=Price4Trd-Slippage
		# �޼�ƽ��
		elif Price<=Price4Trd and Direction==0:
			PriceMatching=Price4Trd
		else:
			return 0,'�۸񲻺��ʣ�δ�ܳɽ�',{'PriceMatching':0,'VolumeMatching':0}
		# �ɽ����ȶ�
		# ȫ���ɽ�
		if VolumeNotMatched<=Volume4Trd:
			VolumeMatching=VolumeNotMatched
		# ���ֳɽ�
		elif VolumeNotMatched>Volume4Trd:
			VolumeMatching=Volume4Trd
		else:
			return 0,'�ɽ����ȶ�ʱ����',{'PriceMatching':0,'VolumeMatching':0}
		return 1,'',{'PriceMatching':PriceMatching,'VolumeMatching':VolumeMatching}

	# ��϶����Լ������Ͻ��
	def MatchOrderByID(self,OrderID):
		ExchangeServerLogger.info("��϶���:{}".format(OrderID))
		# ��ȡ������Ĵ���͹�̨�ͻ���
		Code,Client=self.GetOrderByID(OrderID,['Code','Account'])
		MktInfo = {'Price4Trd': self.MktSliNow.GetDataByCode(Code, 'Price'),
				   'Volume4Trd': self.MktSliNow.GetDataByCode(Code, 'Volume4Trd')}
		ret, msg, MatchInfo = self.MatchSimulation(OrderID, MktInfo)
		# �ж��Ƿ�ɽ�
		if MatchInfo['VolumeMatching'] == 0:
			return 1, '�޳ɽ�'
		# �����Ͻ��
		# OrderPool����
		ret,OrderState = self.DealMatchRetInOrderPool(OrderID, MatchInfo)
		ExchangeServerLogger.debug("OrderPool����:{},{},{}".format(OrderID,ret, OrderState))
		# �г�������ƬҲҪ�����Ͻ�����۳��ɽ����ȣ�
		self.MktSliNow.DealMatchRet(Code, MatchInfo)
		# ���ɳɽ�ʱ��
		MatchTime = self.CreateMatchTime()
		# ֪ͨ��̨����ɽ��ر�
		self.SendTransactionReturn(OrderID, Client, MatchInfo, OrderState, MatchTime)
		return 1,''

	# ��������
	def CancelOrder(self,OrderID,Client):
		ExchangeServerLogger.info("��������:{}".format(OrderID))
		# ���ɳ���ʱ��
		CancelTime=self.CreateCancelTime()
		# ��鳷���Ƿ���Ч
		ret,msg=self.CheckCancelOrder(OrderID,Client)
		ExchangeServerLogger.debug("��鳷���Ƿ���Ч:{},{}".format(ret,msg))
		if ret==0:
			self.SendCancelOrderReturn(Client,OrderID,ret,msg,CancelTime)
			return 0,'����ʧ��'
		# ɾ������
		ret,msg=self.DelOrderByID(OrderID)
		if ret==1:
			msg='�����ɹ�'
		# ���ͳ����ر�
		self.SendCancelOrderReturn(Client,OrderID,ret,msg,CancelTime)

	# ��鳷����Ϣ
	def CheckCancelOrder(self,OrderID,Client):
		if Client.AccountID==None:
			return 0,'�˻�ID�쳣'
		if OrderID not in self.OrderPool:
			return 0,'��Ч��������'
		return 1,'��鳷���ɹ�'

	# ��ȡ����ID�б�
	def GetOrderIDList(self):
		return list(self.OrderPool.columns)

	# ���������ˣ�Ҫ�𶩵���ʼ���
	def OnNewQuoteComing(self):
		ExchangeServerLogger.debug("����������,�𶩵���ʼ���")
		# ��ȡ�����б�
		OrderIDList=self.GetOrderIDList()
		# ��ʼ�𶩵����
		for OrderID in OrderIDList:
			self.MatchOrderByID(OrderID)



if __name__=='__main__':
	Init()