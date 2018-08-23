#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WindSing'

####################################### 导入模块 #######################################################################
import DataModify
import DataDef
from enum import Enum
import datetime
import pandas as pd
import pymssql
####################################### 常量定义 #######################################################################
K_DAY_FIELDS=['open','high','close','low','volume','amount']
# 这个变量用于把标准化的FIELDS转化成Tushare能识别的变量(此处用的是老高频的字段)
TUSHARE_K_DAY_TRAN_FIELDS={DataDef.FIELDS_K_DAY.OP.value:'startprc',
						   DataDef.FIELDS_K_DAY.HP.value:'highprc',
						   DataDef.FIELDS_K_DAY.CP.value:'endprc',
						   DataDef.FIELDS_K_DAY.LP.value:'lowprc',
						   DataDef.FIELDS_K_DAY.VOL.value:'mintq',
						   DataDef.FIELDS_K_DAY.Amount.value:'mintm'
						   }

####################################### 类定义 ########################################################################
class MSSQL:
	def __init__(self,host,user,pwd,db):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db

	def __GetConnect(self):
		if not self.db:
			raise(NameError,"没有设置数据库信息")
		self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
		cur = self.conn.cursor()
		if not cur:
			raise(NameError,"连接数据库失败")
		else:
			return cur

	def ExecQuery(self,sql):
		sql=sql.encode('utf-8')
		cur = self.__GetConnect()
		cur.execute(sql)
		resList = cur.fetchall()

		#查询完毕后必须关闭连接
		self.conn.close()
		return resList

	def ExecNonQuery(self,sql):
		cur = self.__GetConnect()
		cur.execute(sql)
		self.conn.commit()
		self.conn.close()
####################################### 函数定义 #######################################################################
# 最主要的提取数据的函数
def Get_K_TRDMIN_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]

	StartDBName=str(TimeList.StartDate.year)+'{:0>2d}'.format(TimeList.StartDate.month)
	EndDBName=str(TimeList.EndDate.year)+'{:0>2d}'.format(TimeList.EndDate.month)

	TempDB_Date=TimeList.StartDate
	while TempDB_Date<TimeList.EndDate:
		TempDB_Name=str(TempDB_Date.year)+'{:0>2d}'.format(TempDB_Date.month)
		print(TempDB_Name)
		TempDB_Date=TempDB_Date+datetime.timedelta()

	TempDB=MSSQL('192.168.103.172','GTA_QDB','GTA_QDB','GTA_SEL1_TRDMIN_201701')
	# 这里传过来的参数和字段时间轴等都是规则化之后的了，这部分需要加上接独特的处理


	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,[x.FullCode for x in CodeList],DataDef.GROUP_BY_TYPE.CODE.value)
	return Ret,RetValue
# 取到STOCK_BASIC的处理

# 取全部字段的处理
def GetAllFields(DataType):
	if DataType==DataDef.DATA_TYPE.K_DAY.value:
		RetValue=list(TUSHARE_K_DAY_TRAN_FIELDS.keys())
		RetValue.remove('Amount')
	elif DataType==DataDef.DATA_TYPE.STOCK_BASIC.value:
		# RetValue=list(TUSHARE_STOCK_BASIC_TRAN_FIELDS.keys())
		pass
	return RetValue

######################################## 主程序 ########################################################################
if __name__=='__main__':
	Code=DataModify.CodeListModify(['000001.SZ','600000.SH'])
	TimeList=DataModify.TimeListModify(['2017-01-01','2017-02-20'])
	A,B=Get_K_TRDMIN_Data(Code,TimeList,['CP'])

	A=MSSQL('192.168.103.172','GTA_QDB','GTA_QDB','GTA_SEL1_TRDMIN_201701')
	sql='SELECT TOP 1000  SECCODE,SECNAME,TDATE,MINTIME,ENDPRC FROM [dbo].[SZL1_TRDMIN60_201701] WHERE SECCODE in (000001,600000) AND TDATE BETWEEN \'20170101\' AND \'20170130\''
	print(sql)
	Ret=A.ExecQuery(sql)
	Ret=pd.DataFrame(Ret,columns=['SECCODE','SECNAME','TDATE','MINTIME','ENDPRC'])
	a=1

	pass