## My Quant System
---
>该文件用于记录我在建立自己的QuantSystem过程中的一些乱七八糟的记录，先写在这里，日后修改。

- 20170823:功能全部模块化，常用功能函数化，编程语言还在考量中，有没必要用C++，还是直接用Python，觉得还是直接用Python可能比较合适。

	- 策略模块
	- 交易模块
	- 数据模块
	- 回测模块
	- 资管模块：主要接入回测，模拟交易和真实交易的撮合系统。
	- 风控模块：主要接入回测，模拟交易和真实交易的撮合系统。
	* 所有的核心模块都要定义数据的输入输出形式，核心模块之间用一些简单的数据处理模块连接
	* 例如：一个策略模块，首先定义数据输入输出形式，通过不同的数据处理脚本连接不同的数据源，数据模块同理，用作自己的数据仓库，对接不同的实时行情模块。
	- 总流程：Data Generator -> Singal Generator -> BackTest Modular -> Investment Performance Metrics

- 20170824：下一步会继续确定坑能需要定义的类。


### 回测模块

---

1.主要是配合策略模块使用。
2.机制包括逐条循环和向量处理，逐条循环比较好理解，就按照这个方向做下去。
3.以QT为例谈谈回测功能：
	-交易延迟，市场参与度，交易成本，成交价格，滑点，绩效展示
	回测方式：逐笔撮合（是这样宣传的），具体说来可能就是：
		- 提取所需数据：
		- 开始回测-数据输入策略模块->输出交易信息->算法交易系统->虚拟交易所->返回成交数据->记录成交数据->生成委托和持仓数据
		- 循环直到区间结束
		- 统计回测的绩效等。
4.回测系统的组成
	- 回测数据提取
	- 数据输入具体策略
	- 策略完成后进入仿真交易系统
	- 交易及持仓数据统计
	- 回测完成，数据统计，包括绩效统计等
5.以上是构建一个具体的回测系统的一点思路，还有的是涉及到对接其他平台的回测系统，一般说来在平台回测是这样一个逻辑：
	- 策略开始-按照平台api提取平台数据->使用平台api构建策略,输出指定样式的数据或者直接使用下单交易的api->回测系统
	这样极其不方便策略的移植等，而我的想法是这样的：
	- 策略开始->需求数据->数据模块（包括本地数据和各种数据接口）->具体策略内容->输出标准定义的交易数据->转化成平台需求的数据形式->平台回测系统


### 策略模块

---

1.策略模块是最核心的一个模块，也是整个系统能够移植的关键。
2.以QT为例谈谈策略主文件的一个功能。
	- 输入数据：decisiondata(决策数据)；stateMatrix(保存记录的数据)
	- 输出数据：portifilio（投组权重或目标持仓），或者在主函数中直接下单；NewStateMatrix(新纪录的数据)。
	- 主函数中能实现的功能：
		- 持仓查询
		- 其他数据的提取
		- 交易
3.一个策略的策略函数文件需要完成的事情其实就这么多，总结一下一个策略的组成
	- 数据输入：最新决策数据+记录数据+其他数据+持仓数据
	- 条件生成/交易规则
	- 数据输出：需要记录的数据+目标仓位

### 数据模块

---

1.主要内容包括数据输入输出及储存。
2.储存主要涉及一些不好获取的数据，针对个人的话要求数据量还不大。
2.数据输入输出主要指的是来自于其他模块的标准化数据请求通过本地数据或转化成其他数据接口的提取方法获取，然后转化为标准类型输出给需求端口。
