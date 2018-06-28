#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'WindSing'
import time
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import PyMod.Main as BT_Main

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
		Data=[1,2,3,4]
		global count
		t = Event_DataFeed.Value['Date']
		count+=1
		socketio.emit('server_response',
						  {'data': [t,*Data], 'count': count},
						  namespace='/testChartMod') # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
WebChart=RealTimeWebChart()

# 后台线程 产生数据，即刻推送至前端
def background_thread():
	"""Example of how to send server generated events to clients."""
	BT_Main.Main(WebChart)

@app.route('/')
def index():
	return render_template('test.html', async_mode=socketio.async_mode)

# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/testChartMod')
def test_connect():
	global thread
	# for i in range(1,2):
	with thread_lock:
		if thread is None:
			thread = socketio.start_background_task(target=background_thread)


def Main():
	socketio.run(app, debug=True)#,host='127.0.0.1',port='5060')


if __name__ == '__main__':
	Main()