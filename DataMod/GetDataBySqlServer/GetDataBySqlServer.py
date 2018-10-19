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
from CommonMod import GetDateDelta
import decimal
####################################### 常量定义 #######################################################################
K_DAY_FIELDS=['SYMBOL','SHORTNAME','MARKET','TRADINGDATE','OPENPRICE','HIGHPRICE','CLOSEPRICE','LOWPRICE','VOLUME','AMOUNT','LIMITUP','LIMITDOWN'] # 财库的日线行情数据居然没有market，呵呵哒
K_TRDMIN_FIELDS=['seccode','secname','market','tdate','mintime','startprc','highprc','endprc','lowprc','mintq','mintm']
# 这个变量用于把标准化的FIELDS转化成Tushare能识别的变量(此处用的是老高频的字段)
SQLSERVER_K_DAY_TRAN_FIELDS={DataDef.FIELDS_K_DAY.Code.value:"SYMBOL",
							 DataDef.FIELDS_K_DAY.Name.value:"SHORTNAME",
							 DataDef.FIELDS_K_DAY.Exchange.value:"'MARKET'",
							 DataDef.FIELDS_K_DAY.DateTime.value:"cast(TRADINGDATE as datetime)",
							 DataDef.FIELDS_K_DAY.OP.value:"cast(OPENPRICE as float)",
							 DataDef.FIELDS_K_DAY.HP.value:"cast(HIGHPRICE as float)",
							 DataDef.FIELDS_K_DAY.CP.value:"cast(CLOSEPRICE as float)",
							 DataDef.FIELDS_K_DAY.LP.value:"cast(LOWPRICE as float)",
							 DataDef.FIELDS_K_DAY.VOL.value:"cast(VOLUME as float)",
							 DataDef.FIELDS_K_DAY.Amount.value:"cast(AMOUNT as float)",
							 DataDef.FIELDS_K_DAY.Price_LimitUp.value:"cast(LIMITUP as float)",
							 DataDef.FIELDS_K_DAY.Price_LimitDown.value:"cast(LIMITDOWN as float)"
						   }
SQLSERVER_K_MIN_TRAN_FIELDS={DataDef.FIELDS_K_MIN.Code.value:"seccode",
						    DataDef.FIELDS_K_MIN.Name.value:"secname",
						    DataDef.FIELDS_K_MIN.Exchange.value:"CASE market WHEN 'SSE' THEN 'SHSE' ELSE 'SZSE' end",
						    DataDef.FIELDS_K_MIN.DateTime.value:"cast(tdate+' '+stuff(mintime, 3, 0,':') as datetime)",
						    DataDef.FIELDS_K_MIN.OP.value:"cast(startprc as float)",
						    DataDef.FIELDS_K_MIN.HP.value:"cast(highprc as float)",
						    DataDef.FIELDS_K_MIN.CP.value:"cast(endprc as float)",
						    DataDef.FIELDS_K_MIN.LP.value:"cast(lowprc as float)",
						    DataDef.FIELDS_K_MIN.VOL.value:"cast(mintq as float)",
						    DataDef.FIELDS_K_MIN.Amount.value:"cast(mintm as float)"
						   }

####################################### 类定义 ########################################################################
class MSSQL:
	def __init__(self,host,user,pwd,db,port):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db
		self.port=port

	def __GetConnect(self):
		if not self.db:
			raise(NameError,"没有设置数据库信息")
		self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8",port=self.port)
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
# 提取分时数据
def Get_K_MIN_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	if "Code" not in Fields:Fields.append("Code")
	if "Exchange" not in Fields:Fields.append("Exchange")
	if "DateTime" not in Fields:Fields.append("DateTime")
	# 筛选出日频数据取日频接口获取
	Fields_Not_In_K_MIN=[x for x in Fields if x not in SQLSERVER_K_MIN_TRAN_FIELDS.keys()]
	Fields_K_DAY=[x for x in Fields_Not_In_K_MIN if x in SQLSERVER_K_DAY_TRAN_FIELDS.keys()]
	if Fields_K_DAY!=[]:Ret_K_DAY,RetValue_K_DAY=Get_K_DAY_Data(CodeList,TimeList,Fields_K_DAY,SpecialConfig)
	Fields=[x for x in Fields if x in SQLSERVER_K_MIN_TRAN_FIELDS.keys()]
	# 筛选完毕
	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	MonthRange=GetDateDelta.monthRange(TimeList.StartDateStr,TimeList.EndDateStr)
	TempRetValue=pd.DataFrame()
	SpecialConfig=SpecialConfig['K_MIN']
	for TempMonth in MonthRange:
		TempDB_Name=SpecialConfig['DB_Name']+'_'+TempMonth.replace('-','')
		TempDB=MSSQL(SpecialConfig['IP'],SpecialConfig['User'],SpecialConfig['Pwd'],TempDB_Name,SpecialConfig['Port'])
		# 设置Sql语句
		# 1、查SHSE
		TempCode="("+",".join([x.Code for x in CodeList if x.Exchange=='SHSE'])+")"
		TempFields=",".join([SQLSERVER_K_MIN_TRAN_FIELDS[x]+" AS "+x for x in Fields])
		TempTable='SHL1_TRDMIN01_'+TempMonth.replace('-','')
		Sql="SELECT "+ TempFields + " "+ \
			"FROM " + TempTable+ \
			" WHERE "+ \
			"SECCODE IN "+TempCode +" AND "+ \
			"TDATE >'"+ TimeList.StartDateStr +"' AND " + \
			"TDATE <'"+ TimeList.EndDateStr + "'"
		ret=TempDB.ExecQuery(Sql)
		ret_sse=pd.DataFrame(ret,columns=Fields)
		# 1、查SZSE
		TempCode="("+",".join([x.Code for x in CodeList if x.Exchange=='SZSE'])+")"
		TempFields=",".join([SQLSERVER_K_MIN_TRAN_FIELDS[x]+" AS "+x for x in Fields])
		TempTable='SZL1_TRDMIN01_'+TempMonth.replace('-','')
		Sql="SELECT "+ TempFields + " "+ \
			"FROM " + TempTable+ \
			" WHERE "+ \
			"SECCODE IN "+TempCode +" AND "+ \
			"TDATE >='"+ TimeList.StartDateStr +"' AND " + \
			"TDATE <='"+ TimeList.EndDateStr + "'"
		ret=TempDB.ExecQuery(Sql)
		ret_szse=pd.DataFrame(ret,columns=Fields)
		ret=pd.concat([ret_sse,ret_szse])
		TempRetValue=pd.concat([TempRetValue,ret])
	# 在Sql中处理了# 把查出来的Exchangge换成标准的Exchangge，即SSE->SHSE
	# TempRetValue['Exchange']=TempRetValue['Exchange'].replace('SSE','SHSE')
	TempRetValue=TempRetValue.set_index("DateTime").sort_index()
	# 查完所有数据，开始按代码和交易所分组
	for x in CodeList:
		RetValue.append(TempRetValue[(TempRetValue['Code']==x.Code) & (TempRetValue['Exchange']==x.Exchange)])
	# 这里传过来的参数和字段时间轴等都是规则化之后的了，这部分需要加上接独特的处理


	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,[x.FullCode for x in CodeList],DataDef.GROUP_BY_TYPE.CODE.value)
	# 1、将日频字段和分时字段聚合
	if Fields_K_DAY!=[]:
		for TempIndex in RetValue.ValueIndex:
			RetValue.Value[TempIndex]=pd.merge(RetValue.Value[TempIndex],RetValue_K_DAY.Value[TempIndex],how='outer',on=['Code','Exchange'],left_index=True,right_index=True)
			RetValue.Value[TempIndex]=RetValue.Value[TempIndex].fillna(method='pad')
			RetValue.Value[TempIndex]=RetValue.Value[TempIndex].drop(RetValue.Value[TempIndex].index[[x for x in range(0,RetValue.Value[TempIndex].__len__()) if RetValue.Value[TempIndex].index[x].time()==datetime.time(0,0)]])
	return Ret,RetValue
# 提取日线数据
def Get_K_DAY_Data(CodeList,TimeList,Fields,SpecialConfig={}):
	if "Code" not in Fields:Fields.append("Code")
	if "Exchange" not in Fields:Fields.append("Exchange")
	if "DateTime" not in Fields:Fields.append("DateTime")

	Ret=DataDef.FM_Ret(DataDef.STATUS.SUCCESS.value,'')
	RetValue=[]
	TempRetValue=pd.DataFrame()
	SpecialConfig=SpecialConfig['K_DAY']
	TempDB_Name=SpecialConfig['DB_Name']
	TempDB=MSSQL(SpecialConfig['IP'],SpecialConfig['User'],SpecialConfig['Pwd'],TempDB_Name,SpecialConfig['Port'])
	# 设置Sql语句
	# 1、查SHSE
	TempCode="("+",".join([x.Code for x in CodeList])+")"
	TempFields=",".join([SQLSERVER_K_DAY_TRAN_FIELDS[x]+" AS "+x for x in Fields])
	TempTable='STK_MKT_QUOTATION'
	Sql="SELECT "+ TempFields + " "+ \
		"FROM " + TempTable+ \
		" WHERE "+ \
		"SYMBOL IN "+TempCode +" AND "+ \
		"TRADINGDATE >='"+ TimeList.StartDateStr +"' AND " + \
		"TRADINGDATE <='"+ TimeList.EndDateStr + "'"
	ret=TempDB.ExecQuery(Sql)
	ret=pd.DataFrame(ret,columns=Fields)
	#不需要了，现在在数据库中转化了 # 把Decimal类型的转换成float类型的
	# tempcolumns=[x for x in ret.columns if type(ret[x][0])==decimal.Decimal]
	# ret[tempcolumns]=ret[tempcolumns].astype('float64')
	TempRetValue=pd.concat([TempRetValue,ret])
	# 查完所有数据，开始按代码和交易所分组
	for x in CodeList:
		TempDF=TempRetValue[(TempRetValue['Code']==x.Code)]
		TempDF['Exchange']=TempDF['Exchange'].replace('MARKET',x.Exchange)
		TempDF=TempDF.set_index("DateTime").sort_index()
		RetValue.append(TempDF)
	# 这里传过来的参数和字段时间轴等都是规则化之后的了，这部分需要加上接独特的处理


	# 到此数据已经按字段删选完毕了，接下来返回一个结构体，包含数据，组织方式等信息
	RetValue=DataModify.FM_Data(RetValue,[x.FullCode for x in CodeList],DataDef.GROUP_BY_TYPE.CODE.value)
	return Ret,RetValue
# 取全部字段的处理
def GetAllFields(DataType):
	if DataType==DataDef.DATA_TYPE.K_DAY.value:
		RetValue=list(SQLSERVER_K_DAY_TRAN_FIELDS.keys())
	elif DataType==DataDef.DATA_TYPE.STOCK_BASIC.value:
		# RetValue=list(TUSHARE_STOCK_BASIC_TRAN_FIELDS.keys())
		pass
	elif DataType==DataDef.DATA_TYPE.K_TRDMIN.value:
		RetValue=list(SQLSERVER_K_MIN_TRAN_FIELDS.keys())
	return RetValue

######################################## 主程序 ########################################################################
if __name__=='__main__':
	Code=DataModify.CodeListModify(['000001.SZ','600000.SH',"600060.SH"])
	TimeList=DataModify.TimeListModify(['2016-01-01','2016-02-20'])
	# A,B=Get_K_TRDMIN_Data(Code,TimeList,['CP','Name','Code','Exchange','Date','Time'],{'IP':'192.168.103.172','Port':1433,'User':'GTA_QDB','Pwd':'GTA_QDB'})
	# A,B=Get_K_TRDMIN_Data(Code,TimeList,['CP','Name','Code','Exchange','Date','Time'],{'IP':'127.0.0.1','Port':1433,'User':'windsing','Pwd':'199568','DB_Name':'SHSE_MIN'})
	# A,B=Get_K_DAY_Data(Code,TimeList,['CP','Name','Code','Exchange','Date','Price_LimitUp','Price_LimitDown'],{'IP':'10.223.26.156','Port':2433,'User':'GTA_QDB','Pwd':'GTA_QDB'})
	A,B=Get_K_DAY_Data(Code,TimeList,['CP','Name','Code','Exchange','Date','Price_LimitUp','Price_LimitDown'],{'IP':'127.0.0.1','Port':1433,'User':'windsing','Pwd':'199568','DB_Name':'K_DAY_DATA'})

	A=MSSQL('192.168.103.172','GTA_QDB','GTA_QDB','GTA_SEL1_TRDMIN_201701')
	sql='SELECT TOP 1000  SECCODE,SECNAME,TDATE,MINTIME,ENDPRC FROM [dbo].[SZL1_TRDMIN60_201701] WHERE SECCODE in (000001,600000) AND TDATE BETWEEN \'20170101\' AND \'20170130\''
	print(sql)
	Ret=A.ExecQuery(sql)
	Ret=pd.DataFrame(Ret,columns=['SECCODE','SECNAME','TDATE','MINTIME','ENDPRC'])
	a=1

	pass