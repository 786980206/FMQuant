// 设置端口
@[system;"p 9568";{-2"端口打开失败",x,
	 	     "请确认端口未被占用",
		     " 或切换至其他端口";  
		     exit 1}]
	
// 切换回根目录
\d .
// 建立分时行情的表
fmq_sts:([]time:`timestamp$();
        sym:`$();
        o:`float$();
        h:`float$();
        l:`float$();
        c:`float$();
        v:`float$();
        m:`float$();
        sp1:`float$();
        sp2:`float$();
        sp3:`float$();
        sp4:`float$();
        sp5:`float$();
        bp1:`float$();
        bp2:`float$();
        bp3:`float$();
        bp4:`float$();
        bp5:`float$();
        sv1:`float$();
        sv2:`float$();
        sv3:`float$();
        sv4:`float$();
        sv5:`float$();
        bv1:`float$();
        bv2:`float$();
        bv3:`float$();
        bv4:`float$();
        bv5:`float$()       
        )

// 加载u.q
\l w32/tick/u.q
.u.init[]
	


// 消息推送示例
sts_sp:([]time:`timestamp$(enlist 2019.7.10T21:40:55);
        sym:`$(enlist "000001.SZSE");
        o:`float$(enlist 10);
        h:`float$(enlist 11);
        l:`float$(enlist 9);
        c:`float$(enlist 10.5);
        v:`float$(enlist 10000);
        m:`float$(enlist 100000);
        sp1:`float$(enlist 10.5);
        sp2:`float$(enlist 10.6);
        sp3:`float$(enlist 10.7);
        sp4:`float$(enlist 10.8);
        sp5:`float$(enlist 10.9);
        bp1:`float$(enlist 10.4);
        bp2:`float$(enlist 10.3);
        bp3:`float$(enlist 10.2);
        bp4:`float$(enlist 10.1);
        bp5:`float$(enlist 10);
        sv1:`float$(enlist 100);
        sv2:`float$(enlist 100);
        sv3:`float$(enlist 100);
        sv4:`float$(enlist 100);
        sv5:`float$(enlist 100);
        bv1:`float$(enlist 100);
        bv2:`float$(enlist 100);
        bv3:`float$(enlist 100);
        bv4:`float$(enlist 100);
        bv5:`float$(enlist 100)       
        )
\
.u.pub[`fmq_sts;sts_sp]
.z.ts:{.u.pub[`fmq_sts;sts_sp]}
\t 10