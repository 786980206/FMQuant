import datetime
import numpy
import random
import threading
import sys
import time

from qpython import qconnection
from qpython.qcollection import qlist
from qpython.qtype import QException, QTIME_LIST, QSYMBOL_LIST, QFLOAT_LIST,QGUID_LIST,QDATETIME_LIST,QINT_LIST


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

class Q(qconnection.QConnection):
	# 基础查询
	def Exec(self,Str):
		try:
			ret=q(str(Str),pandas=True)
			return ret
		except Exception as e:
			print(e)
			return None
	# 类型转换
	def TypeConvert(self,VauleList,TypeList):
		ValueList=[Func(VauleList[TypeList.index(Func)]) for Func in TypeList]
		return  ValueList

	# 转化成SymbolList
	def ToSymbolList(self,List):
		List = [str(x) for x in List]
		return "`{}".format("`".join(List))
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

	# 查询表格
	def Query(self,Str):
		try:
			df=q(str(Str),pandas=True)
			return df
		except Exception as e:
			print(e)
			return None

	# 插入数据
	def Insert(self,TableName,ValueList,TypeList):
		ValueList=self.TypeConvert(ValueList,TypeList)
		ValueList=';'.join(ValueList)
		AimStr="`{} insert({})".format(TableName,ValueList)
		print(AimStr)
		self.Exec(AimStr)

	# 删除数据
	def Del(self,Str):
		pass




if __name__ == '__main__':
	# with qconnection.QConnection(host='localhost', port=9568) as q:
	import uuid,datetime
	with Q(host='localhost', port=9568,numpy_temporals = True) as q:
		q.Exec("s:([X:`$()]A:`float$();B:`guid$();C:`datetime$())")
		q.Insert("s",[[1,2],[3,4],[uuid.uuid1()]*2,[datetime.datetime.now()]*2],[q.ToSymbolList,q.ToFloatList,q.ToGuidList,q.ToDateTimeList])

