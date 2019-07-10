// load in u.q from tick
upath:"w32/tick/u.q"
@[system;"l ",upath;{-2"Failed to load u.q from ",x," : ",y, 
		       ". Please make sure u.q is accessible.",
                       " kdb+tick can be downloaded from http://code.kx.com/wsvn/code/kx/kdb+tick";
		       exit 2}[upath]]

// initialise pubsub 
// all tables in the top level namespace (`.) become publish-able
// tables that can be published can be seen in .u.w
.u.init[]
ask:([]time:`symbol$(); sym:`symbol$();test1:`symbol$();Price:`float$())



/`初始化脚本
show `$"FMQuant DataServer Init...";

/`建表：Postion,OrderList,CashInfo,Account,k_StsPerTick
show `$"Creat Table..."

/`Exchange的订单池表
Exchange_OrderPool:([AccountID:`guid$();OrderID:`guid$()]Code:`symbol$();Direction:`int$();Price:`float$();Volume:`int$();VolumeMatched:`int$();State:`symbol$();AvgMatchingPrice:`float$();OrderTime:`datetime$();Mkt:`symbol$();AddPar:`symbol$());

/`Exchange的连接信息表
Exchange_ConnectInfo:([ClientID:`guid$()]Usr:`symbol$();AccountID:`guid$();ConnectState:`int$();Addr:`$();ConnectTime:`datetime$());

/`Client的持仓信息表
Client_Position:([AccountID:`guid$();Code:`symbol$()]Vol:`int$();VolA:`int$();VolF:`int$();StockActualVol:`int$();AvgCost:`float$();PriceNow:`float$();MktValue:`float$();FloatingProfit:`float$();ProfitRatio:`float$();Currency:`symbol$();Mkt:`symbol$();AddPar:`symbol$());

/`Client的订单信息表
Client_Order:([AccountID:`guid$();OrderID:`guid$()]Code:`symbol$();Direction:`int$();Price:`float$();Volume:`int$();VolumeMatched:`int$();State:`symbol$();AvgMatchingPrice:`float$();OrderTime:`datetime$();Mkt:`symbol$();AddPar:`symbol$());

/`Client的订单全量表
Client_OrderRec:([AccountID:`guid$();OrderID:`guid$()]Code:`symbol$();Direction:`int$();Price:`float$();Volume:`int$();VolumeMatched:`int$();State:`symbol$();AvgMatchingPrice:`float$();OrderTime:`datetime$();Mkt:`symbol$();AddPar:`symbol$());

/`Client的资金信息表
Client_CashInfo:([AccountID:`guid$()]Cash:`float$();CashF:`float$();CashA:`float$();InitCash:`float$());

Position:([Code:`symbol$()]Vol:`int$();VolA:`int$();VolFrozen:`int$();StockActualVol:`int$();AvgCost:`float$();PriceNow:`float$();MktValue:`float$();FloatingProfit:`float$();ProfitRatio:`float$();Currency:`symbol$();Mkt:`symbol$();AccountID:`guid$();AddPar:`symbol$());

OrderList:([OrderID:`guid$()]Code:`symbol$();Direction:`int$();Price:`float$();Volume:`int$();VolumeMatched:`int$();State:`symbol$();AvgMatchingPrice:`float$();OrderTime:`datetime$();Mkt:`symbol$();AccountID:`guid$();AddPar:`symbol$());



CashInfo:([AccountID:`guid$()]Cash:`float$();CashF:`float$();CashA:`float$();InitCash:`float$());

Account:([Usr:`symbol$()]Pwd:`symbol$();AccountID:`guid$();ConnectState:`int$());

k_StsPerTick:([Code:`symbol$()]TradingTime:`datetime$();BP1:`float$();BV1:`float$();SP1:`float$();SV1:`float$();BP2:`float$();BV2:`float$();SP2:`float$();SV2:`float$();BP3:`float$();BV3:`float$();SP3:`float$();SV3:`float$();BP4:`float$();BV4:`float$();SP4:`float$();SV4:`float$();BP5:`float$();BV5:`float$();SP5:`float$();SV5:`float$();BP6:`float$();BV6:`float$();SP6:`float$();SV6:`float$();BP7:`float$();BV7:`float$();SP7:`float$();SV7:`float$();BP8:`float$();BV8:`float$();SP8:`float$();SV8:`float$();BP9:`float$();BV9:`float$();SP9:`float$();SV9:`float$();BP10:`float$();BV10:`float$();SP10:`float$();SV10:`float$());

/`没找到怎么把一个字段定义成序列的方法
/`初始化数据
show `$"Data init..."
`Account insert (`windsing`Usr`root;`199568`Pwd`root;"G"$("44c12f24-68d4-11e9-92f0-08606e0f5471";"50d1dd40-68d4-11e9-b96e-08606e0f5471";"5753d902-68d4-11e9-a281-08606e0f5471");0 0 0);
`CashInfo insert ("G"$("44c12f24-68d4-11e9-92f0-08606e0f5471";"50d1dd40-68d4-11e9-b96e-08606e0f5471";"5753d902-68d4-11e9-a281-08606e0f5471");1000000.0 1000000.0 1000000.0;0.0 0.0 0.0;1000000.0 1000000.0 1000000.0;0.0 0.0 0.0);

`Client_CashInfo insert ("G"$("d09e1270-f38d-35f0-aad3-e23d2b2354e7");1000000.0;0.0;1000000.0 ; 0.0);


/`启动服务
\p 9568

/`初始化一张测试表
t:([Guid:"G"$()]Int:`int$();Float:"f"$();Symbol:`$();DateTime:`datetime$());
`t insert("G"$"44c12f24-68d4-11e9-92f0-08606e0f5471";1;10.1;`ABC;2019.04.25T12:24:30.789);
`t insert("G"$"50d1dd40-68d4-11e9-b96e-08606e0f5471";1;10.1;`ABC;2019.04.25T13:24:30.123);
s:([]a:());
`s insert(123);

show `$"Start Successful!"