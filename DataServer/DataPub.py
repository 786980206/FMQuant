# coding=utf-8
import datetime
import numpy as np
import random
import threading
import sys
import time

from qpython import qconnection
from qpython.qcollection import qlist,qtable
from qpython.qtype import QException, QTIME_LIST, QSYMBOL_LIST, QFLOAT_LIST,QTIMESTAMP_LIST


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
            # print('.')
            try:
                # publish data to tick
                # function: .u.upd
                # table: ask
                self.q.sendSync('.u.pub', np.string_('fmq_sts'), self.get_ask_data())
                print("发送成功!")
                #time.sleep(1)
            except Exception as e:
                print("出错了...")
                print(e)

    def get_ask_data(self):
        time=qlist(np.array([np.datetime64('2018-02-01T22:43:40')]),qtype=QTIMESTAMP_LIST)
        sym=qlist(np.array(["000001.SZSE"]),qtype=QSYMBOL_LIST)
        o=qlist(np.array([10]),qtype=QFLOAT_LIST)
        h=qlist(np.array([11]),qtype=QFLOAT_LIST)
        l=qlist(np.array([9]),qtype=QFLOAT_LIST)
        c=qlist(np.array([10.5]),qtype=QFLOAT_LIST)
        v=qlist(np.array([10000]),qtype=QFLOAT_LIST)
        m=qlist(np.array([100000]),qtype=QFLOAT_LIST)
        sp1=qlist(np.array([10.5]),qtype=QFLOAT_LIST)
        sp2=qlist(np.array([10.6]),qtype=QFLOAT_LIST)
        sp3=qlist(np.array([10.7]),qtype=QFLOAT_LIST)
        sp4=qlist(np.array([10.8]),qtype=QFLOAT_LIST)
        sp5=qlist(np.array([10.9]),qtype=QFLOAT_LIST)
        bp1=qlist(np.array([10.4]),qtype=QFLOAT_LIST)
        bp2=qlist(np.array([10.3]),qtype=QFLOAT_LIST)
        bp3=qlist(np.array([10.2]),qtype=QFLOAT_LIST)
        bp4=qlist(np.array([10.1]),qtype=QFLOAT_LIST)
        bp5=qlist(np.array([10]),qtype=QFLOAT_LIST)
        sv1=qlist(np.array([100]),qtype=QFLOAT_LIST)
        sv2=qlist(np.array([100]),qtype=QFLOAT_LIST)
        sv3=qlist(np.array([100]),qtype=QFLOAT_LIST)
        sv4=qlist(np.array([100]),qtype=QFLOAT_LIST)
        sv5=qlist(np.array([100]),qtype=QFLOAT_LIST)
        bv1=qlist(np.array([100]),qtype=QFLOAT_LIST)
        bv2=qlist(np.array([100]),qtype=QFLOAT_LIST)
        bv3=qlist(np.array([100]),qtype=QFLOAT_LIST)
        bv4=qlist(np.array([100]),qtype=QFLOAT_LIST)
        bv5=qlist(np.array([100]),qtype=QFLOAT_LIST)
        data=qtable(("time","sym","o","h","l","c","v","m","sp1","sp2","sp3","sp4","sp5","bp1","bp2","bp3","bp4","bp5","sv1","sv2","sv3","sv4","sv5","bv1","bv2","bv3","bv4","bv5"),[time,sym,o,h,l,c,v,m,sp1,sp2,sp3,sp4,sp5,bp1,bp2,bp3,bp4,bp5,sv1,sv2,sv3,sv4,sv5,bv1,bv2,bv3,bv4,bv5])
        print(data)
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