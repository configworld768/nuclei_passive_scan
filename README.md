# nuclei_passive_scan
基于nuclei的简单被动扫描实现<br>

## 使用mitmproxy实现的，基本思路就是使用mitm监听一个端口，浏览器挂上mitm的代理手动点击或者使用selenium来跑，url信息存入redis的队列中<br>
## python启动nuclei扫描脚本从redis队列中获取扫描资产
