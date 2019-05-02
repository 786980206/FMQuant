import sys
sys.path.append("..\\PyMod")
import datetime
import numpy
import random
import threading
import sys
import time
import pandas as pd
from qpython import qconnection
from qpython.qcollection import qlist
from qpython.qtype import QException, QTIME_LIST, QSYMBOL_LIST, QFLOAT_LIST,QGUID_LIST,QDATETIME_LIST,QINT_LIST
import json
import Common as cm
import GeneralMod


class PublisherThread(threading.Thread):

	def __init__(self, q):
		super(PublisherThread, self).__init__()
		self.q = q
		self._stopper = threading.Event()

	def stop(self):
		self._stopper.set()

	def stopped(self):
		return self._stopper.isSet()

	def run(self):
		while not self.stopped():
			print('.')
			try:
				# publish data to tick
				# function: .u.upd
				# table: ask
				self.q.sendSync('.u.upd', numpy.string_('ask'), self.get_ask_data())
				print("Success!")
				time.sleep(1)
			except QException as e:
				print(e)
			except:
				self.stop()

	def get_ask_data(self):
		c = random.randint(1, 10)

		today = numpy.datetime64(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

		time = [numpy.timedelta64((numpy.datetime64(datetime.datetime.now()) - today), 'ms') for x in range(c)]
		instr = ['instr_%d' % random.randint(1, 100) for x in range(c)]
		src = ['qPython' for x in range(c)]
		ask = [random.random() * random.randint(1, 100) for x in range(c)]

		data = [qlist(time, qtype=QTIME_LIST), qlist(instr, qtype=QSYMBOL_LIST), qlist(src, qtype=QSYMBOL_LIST), qlist(ask, qtype=QFLOAT_LIST)]
		print(data)
		return data

# Q操作类
class Q(qconnection.QConnection):
	# 初始化
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.SetTable()
		self.open()

	# 绑定表
	def SetTable(self):
		self.Trans={"symbol":self.ToSymbolList,"float":self.ToFloatList,"guid":self.ToGuidList,"datetime":self.ToDateTimeList,"int":self.ToIntList,"json":self.ToJsonList}
		self.Tables={}

	# 添加表
	def AddTable(self, TableName, ColInfo,ColList):
		# ColInfo={"A":"symbol"}
		self.Tables[TableName]={}
		self.Tables[TableName]["ColInfo"]=ColInfo
		ConvertInfo={}
		for x in ColInfo:
			ConvertInfo[x]=self.Trans[ColInfo[x]]
		self.Tables[TableName]["ColConvert"] =ConvertInfo
		self.Tables[TableName]["ColList"]=ColList

	# 基础查询
	def Exec(self,Str):
		try:
			ret=self(str(Str),pandas=True)
			return ret
		except Exception as e:
			print(e)
			return None
	# 类型转换
	def TypeConvert(self,VauleList,Func):
		ValueList=Func(VauleList)

	# 转化成SymbolList
	def ToSymbolList(self,List):
		List = [str(x).replace('"','\\"') for x in List]
		if sum([len(x)==1 for x in List])==len(List):
			return "`{}".format("`".join(List))
		return '''`$("{}")'''.format('''";"'''.join(List))
	# 转化成IntList
	def ToIntList(self, List):
		List = [str(x) for x in List]
		return "`int$({})".format(",".join(List))
	# 转化成FloatList
	def ToFloatList(self, List):
		List = [str(x) for x in List]
		return "`float$({})".format(",".join(List))
	# 转化成GuidList
	def ToGuidList(self, List):
		List=[str(x) for x in List]
		return '''"G"$("{}")'''.format('''";"'''.join(List))
	# 转化成DateTimeList
	def ToDateTimeList(self, List):
		List = [str(x).replace("-",".").replace(" ","T") for x in List]
		return "`datetime${}".format(",".join(List))
	# 转化成DateTimeList
	def ToJsonList(self, List):
		List = [GeneralMod.ToStr(x) for x in List]
		return self.ToSymbolList(List)
	# 单值转化
	def SingleValueTypeConvert(self,value,Type):
		value=[value]
		return self.Trans[Type](value)


	# 新建表
	def CreateTable(self,TableName,ColumesType,ColList,key=None):
		if key==None:key=[]
		Columes=ColList
		TypeList=[ColumesType[x] for x in ColList]
		Temp=self.Row2Col([Columes,TypeList])
		# print(Temp)
		Body=";".join(["{}:`{}$()".format(x[0],x[1]) if x[1]!="symbol" else "{}:`$()".format(x[0]) for x in Temp if x[0] not in key])
		MainKey=";".join(["{}:`{}$()".format(x[0],x[1]) if x[1]!="symbol" else "{}:`$()".format(x[0]) for x in Temp if x[0] in key])
		AimStr="{}:([{}]{})".format(TableName,MainKey,Body)
		self.Exec(AimStr)
		self.AddTable(TableName,ColumesType,ColList=ColList)


	# 查询表格
	def Query(self,TableName:str,Fields:list,Conditions:str="1=1")->pd.DataFrame:
		FieldsStr=",".join(Fields)
		AimStr="""select {} from `{} where {}""".format(FieldsStr,TableName,Conditions)
		pd_ret=self.Exec(AimStr)
		# 格式转化
		# symbol：decode()
		# time：__format__("%Y-%m-%d %H:%M:%S.%f")
		# json:json.loads(Config.decode())
		if Fields==[]:Fields=self.Tables[TableName]["ColList"]
		symbol_fields=[x for x in Fields if self.Tables[TableName]["ColInfo"][x]=="symbol"]
		datetime_fields = [x for x in Fields if self.Tables[TableName]["ColInfo"][x] == "datetime"]
		json_fields=[x for x in Fields if self.Tables[TableName]["ColInfo"][x] == "json"]
		int_fields = [x for x in Fields if self.Tables[TableName]["ColInfo"][x] == "int"]
		foloat_fields=[x for x in Fields if self.Tables[TableName]["ColInfo"][x] == "float"]
		# 转化函数
		symbol_convert=lambda x:x.decode()
		datetime_convert = lambda x: x.__format__("%Y-%m-%d %H:%M:%S.%f")
		json_convert=lambda x:json.loads(x.decode())
		int_convert=lambda x:int(x)
		float_convert=lambda x:float(x)
		# 开始转化
		for x in symbol_fields:
			pd_ret[x]=pd_ret[x].apply(symbol_convert)
		for x in datetime_fields:
			pd_ret[x]=pd_ret[x].apply(datetime_convert)
		for x in json_fields:
			pd_ret[x]=pd_ret[x].apply(json_convert)
		for x in int_fields:
			pd_ret[x]=pd_ret[x].apply(int_convert)
		for x in foloat_fields:
			pd_ret[x]=pd_ret[x].apply(float_convert)
		return pd_ret

	# 插入数据
	def Insert(self,TableName,ValueDict):
		# "A": [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()],
		# "B": [uuid.uuid1(), uuid.uuid1(), uuid.uuid1()],
		# "C": ["A", "B", "C"]
		StrList={}
		AimStr=[self.Tables[TableName]["ColConvert"][x](ValueDict[x]) for x in self.Tables[TableName]["ColList"]]
		AimStr=';'.join(AimStr)
		AimStr="`{} insert({})".format(TableName,AimStr)
		# print(AimStr)
		self.Exec(AimStr)

	# 更新数据
	def Update(self,TableName,ValueDict,Conditions="1=1",Convert=True):
		if Convert:
			ValueList=[self.SingleValueTypeConvert(ValueDict[x],self.Tables[TableName]["ColInfo"][x]) for x in ValueDict]
		else:
			ValueList=[ValueDict[x] for x in ValueDict]
		Columns=[x for x in ValueDict]
		Temp=self.Row2Col([Columns,ValueList])
		Temp=",".join(["{}:{}".format(x[0],x[1]) for x in Temp])
		AimStr="update {} from `{} where {}".format(Temp,TableName,Conditions)
		# print(AimStr)
		self.Exec(AimStr)

	# 删除数据
	def Del(self,TableName,Conditions="1=1"):
		AimStr="delete from `{} where {}".format(TableName,Conditions)
		self.Exec(AimStr)

	# 行转列
	def Row2Col(self,data):
		return list(map(list, zip(*data)))







if __name__ == '__main__':
	# with qconnection.QConnection(host='localhost', port=9568) as q:
	import uuid,datetime
	with Q(host='localhost', port=9568,numpy_temporals = True) as q:
		q.CreateTable("ABCD", {"BBB":"datetime","AAA":"guid", "CCC":"symbol"}, ColList=["AAA","BBB","CCC"],key=["AAA"])
		q.Insert("ABCD",{"BBB":[datetime.datetime.now(),datetime.datetime.now(),datetime.datetime.now()],
						"AAA":[uuid.uuid1(),uuid.uuid1(),uuid.uuid1()],
						"CCC":["A","B","C"]
						})
		q.Del("ABCD","CCC=`B")
		q.Query("ABCD","CCC=`A")
		q.Update("ABCD",{"CCC":"ahahaha"},"CCC=`A")

		q.CreateTable("x", {"a": "symbol", "b": "symbol", "c": "symbol"}, ["a"])
		q.Insert("x", {"a": ["A", "B", "C"],
						  "b":["A", "B", "C"],
						  "c": ["A", "B", "C"]
						  })




