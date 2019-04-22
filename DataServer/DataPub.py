import datetime
import numpy
import random
import threading
import sys
import time

from qpython import qconnection
from qpython.qcollection import qlist
from qpython.qtype import QException, QTIME_LIST, QSYMBOL_LIST, QFLOAT_LIST


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
		# print(data)
		return data


if __name__ == '__main__':
	with qconnection.QConnection(host='localhost', port=9568) as q:
		print(q)
		print('IPC version: %s. Is connected: %s' % (q.protocol_version, q.is_connected()))
		print('Press <ENTER> to close application')

		t = PublisherThread(q)
		t.start()

		sys.stdin.readline()

		t.stop()
		t.join()