AdviceContentCrawler
=====

整体功能
-----
通过python爬虫，快速抓取24万条医疗咨询数据。

文件组成
-----
* DoctorListCrawler，抓取医生的列表
* AdviceListCrawler，抓取每个医生咨询的列表
* AdviceContentCrawler，抓取每个咨询的内容

在每个Crawler中，execute()是最终的执行入口

代码使用的注意事项
------
* 代码在Linux/Mac下编写，所以分割符号是\n，文件夹的分隔符是/，在Windows环境下需要进行修改
* 每个Crawler文件里的文件夹需要修改，以符合你实际的文件夹名称
* 程序在python2.7下运行，在python3上会有一定的问题

抓来了数据应该怎么用
-----
请关注作者的公众账号，上面有具体的产品使用场景
在微信中搜索公众账号altnlp，即将关注该公众账号

如何联系到作者
-----
添加微信 retire2053
