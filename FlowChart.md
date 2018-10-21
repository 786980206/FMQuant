<=示例函数=>
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？
=>st->op->cond
=>cond(yes)->e
=>cond(no)->op
<=示例结束=>
<==========FMQuant==========>
st=>start: 开始
<=Main.py=>
Main.py1=>operation: GeneralMod.LoadJson
#读取配置
StrategyMod.LoadStrategy
#加载策略
EventMod.EventEngine
#初始化事件引擎
CoreEventEngine.Register(EventMod.EVENT_DATAFEED, PushMod.ShowData)
#注册ShowData函数
Main.py2=>condition: WebObj!=None?
#判断是否需要在网页上展示
Main.py3=>operation: CoreEventEngine.Register(EventMod.EVENT_DATAFEED, WebObj.PushData)
#注册推送数据给网页
Main.py4=>condition: Config['BackTestConfig']['ForBackTest']?
#是否用于回测
Main.py5=>operation: BackTestMod.MatchingSys(Strategy,CoreEventEngine,Config)
BackTestMod.DataFeed(MatchingSys)
CoreEventEngine.Register(EventMod.EVENT_DATAFEED,MatchingSys.RefreshQoutation)
#从BackTestMod获取行情
Main.py6=>operation: PushMod.DataFeed(Config['SubConfig'])
#从PushMod获取行情
Main.py7=>operation: CoreEventEngine.Register(EventMod.EVENT_DATAFEED,Strategy.DealFeedData)
CoreEventEngine.Start()
whileMatchingSys.IsRunning:
	#隔5s检测一次是否回测完成
	time.sleep(5)
CoreEventEngine.Stop()
MatchingSys.PerformanceStatistics()
#注册推送数据给策略；事件引擎开启；检测回测是否结束；停止引擎；统计绩效；
ed=>end
<=Main.py=>

st->Main.py1->Main.py2
Main.py2(yes)->Main.py3->Main.py4
Main.py2(no)->Main.py4
Main.py4(yes)->Main.py5->Main.py7
Main.py4(no)->Main.py6->Main.py7->ed




