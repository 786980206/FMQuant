## To Do List
---

- 每日盘后撤单，订单记录要不要加入到DealRec中呢？
	- 感觉要加入，因为目前如果是部分成交的话在完全成交之前还没加入成交记录吗？
	- 如果之前的部分成交加入了的话，这里撤单还要不要加入呢？
	- 目前是加入其中了
- 每次来新行情，需要先撮合一下之前没没有撮合成功的委托，即self.Order，还没做
- 现在还是策略驱动和行情同步驱动，即没有滞后，这个不行，之后可能要考虑在根本上大改了。

- 接下来要做的是DataMod
	- 先把Tushare接进来
- 股票代码的规范也要写进入GeneralMod

- 最后做界面
- 提数功能必须要能够独立调用
	DataMod只是回测部分一个入口，核心功能要在文件夹DataMod中。

- 一般来书证券的行情数据有时间，代码，字段三个维度，时间一般不分割，那么数据就有按代码和按字段两个分割的方式，怎么组织为好呢？
	- QT里面是采用的按字段分割，一个字段一张表的形式
	- Tushare提取历史数据是明显的按照代码分割的
	- 按时间分割有时候研究界面数据也是必要的，有必要进行三种方式转换
	- 按时间分割的话对高频数据研究来说没什么意义，考虑时频之上在引入这个组织形式吧。
	- 目前先按照QT的方式按字段研究
	- 需要定义一个数据类，至少有两个数据，value代表具体数据，还有一个数据描述，例如频率等