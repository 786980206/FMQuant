#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'
import time
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import PyMod.Main as BT_Main
import json

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
count = 0
# RealTimeWebChart的主要对象，作为一个类反馈给回测系统，可以在这里面定义更多的函数
class RealTimeWebChart():
	def __init__(self):
		pass
	def PushTest(self,Data):
		Data=[1,2,3,4]
		global count
		t = time.strftime('%H:%M:%S', time.localtime()) # 获取系统时间（只取分:秒）
		count+=1
		socketio.emit('server_response',
						  {'data': [t,*Data], 'count': count},
						  namespace='/test') # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
	def PushData(self,Event_DataFeed):
		DataX = Event_DataFeed.Value['Date']
		DataValue=[Event_DataFeed.Value['Data']['000001.SZSE'].loc['OP'],
				   Event_DataFeed.Value['Data']['000001.SZSE'].loc['CP'],
				   Event_DataFeed.Value['Data']['000001.SZSE'].loc['HP'],
				   Event_DataFeed.Value['Data']['000001.SZSE'].loc['LP']
				   ]
		DataVol=[DataX,int(Event_DataFeed.Value['Data']['000001.SZSE'].loc['VOL'])]
		if Event_DataFeed.Value['Data']['000001.SZSE'].loc['CP']>Event_DataFeed.Value['Data']['000001.SZSE'].loc['OP']:
			DataVol.append(1)
		else:
			DataVol.append(-1)
		print("---------------------------------------------------------------------------------------------------")

		a={'DataX': DataX,'DataValue':DataValue,'DataVol':DataVol,'count': 0}
		print(a)
		json.dumps(a)
		socketio.emit('server_response',
						  {'DataX': DataX,'DataValue':DataValue,'DataVol':DataVol,'count': 0},
					   # {'data': 10,'DataValue':[40, 40, 32, 42],'DataVol':[str(10),3,-1], 'count': count},
						  namespace='/test') # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
	def PushStockData(self):
		Data=[1,2,3,4]
		global count
		count+=1
		t=count
		socketio.emit('server_response',
						  {'data': [t,[40, 40, 32, 42],[str(t),3,-1]], 'count': count},
						  namespace='/test') # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
WebChart=RealTimeWebChart()

# 后台线程 产生数据，即刻推送至前端
def background_thread():
	global thread
	BT_Main.Main(WebChart)
	# print('----------------------over------------------------------------------------------------------')
	return

@app.route('/')
def index():
	return render_template('RealTimeBT.html', async_mode=socketio.async_mode)

# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/test')
def test_connect():
	print('连接了！！！！！！！！！！！！！！！！！！！')
	# global thread
	# for i in range(1,2):
	with thread_lock:
		# if thread is None:
		thread = socketio.start_background_task(target=background_thread)


def Main():
	socketio.run(app, debug=True)#,host='127.0.0.1',port='6666')


if __name__ == '__main__':
	Main()