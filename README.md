﻿# chatroom-python
my test for computer network

# 2017.5.11
初步的版本提交，距离构想还差gui的绘制，skey协议的部署，邮件确认注册成功，数据库储存密码等功能。

# 2017.5.12
编写成功邮件函数，向注册邮箱之中发送注册成功邮件（未附加图片？）

# 2017.5.13
进行了qt的进一步学习，决定了窗体的大致结构。聊天图片利用爬虫来爬一张美女图？（大污。。。
成功编写爬虫，将图片保存到本地，预期使用随机函数，调用图片。

# 2017.5.16
尝试了连接mysql数据库，成功用pymysql进行了连接，但是貌似不会使用插入时间的功能，对命令行版本进行了修正，发现需要对代码进行重构。
数据库功能决定部署在服务器类中，重载了__enter__和__exit__函数，使用with岂不是美滋滋～
初步尝试界面连接函数，connect得不是很顺利，QMessageBox不会调用？（捂脸逃...

#2017.5.17
QMessageBox使用成功，调用的时候第一个参数应该是父窗口（感受：多看官方文档，文档看不懂再google
ps：pyqt的文档就有错啊，摔！QMessageBox明明在QtWidgets而不在QtGui啊混蛋。。。
clientChat端不能沿用一开始的死等循环，无法将其与GUI连接起来，recvMsg收到信息应该将其返回，然后在客户端的GUI界面进行消息的增加，现在打算使用线程池，对其进行类似UDP的模拟,但是当很多用户同时发送消息的时候，服务器频繁给客户端信息，会造成socket被占用，无法进行正常的信息添加？
其实使用线程池就好了？毕竟最终使用的	是相同的socket（服务器端向客户端进行io传输），但是在线程池队列之中，是不是同时进行的啊，需要查看ThreadPoolExecutor的详细文档，找到线程安全的线程池。

# 2017.5.18
QMessageBox的参数不知道怎么回事，就是无法调用，最后一个参数明明就是QMessageBox.No啥的啊，但是就是报类型错误。
妥协，最后按照最初级的方式，直接不使用子窗口父窗口模式，自己调出来一个新的QMessageBox使用，也能达到同样的效果。
发送socket遇到bug，不知道为什么，在子窗口发送完消息之后，再次发送消息，server端没有收到消息，socket在客户端已经将消息发送出去了啊。
发送完成了，socket客户端已经进入阻塞状态，在等待server的响应了。
理清思路了，由于使用线程池，所以我在一开始提交任务的时候，使用的accept进行的阻塞式提交任务。
阻塞调好了，下面开始进入聊天界面的连接。
聊天界面最烦的是接受消息，我不知道怎么将clientChat的接收消息的函数结合在chatmsg_textEdit之上，他没有相应的动作来对应其扩展啊。
也许，使用clientChat来进行函数驱动？但是没法连接在界面之上啊，没有一个函数是使用事件进行驱动的。

# 2017.5.19
开始着手聊天登录的编写，recv的坑踩了好几次了，recv的死等造成GUI的死等，造成死锁。
今天对skey算法进行了思考，如果客户端使用了skey算法，发送了密码，接收到服务器发送给他的hash链，登录的时候如何输入密码？
暂定的解决方案：将初始密码放置在密码文件的第一个，对比是否正确，然后，在密码文件中遍历行，找到末尾做标记的上一次的密码，使用上一行的密码与服务器进行交互。
改进：不使用skey算法，而改用ECC密钥？
现在纠结问题，如何在开启子窗口的时候将父窗口关闭或者让他隐形。

# 2017.5.20
可怕，在别人都在秀恩爱的时候我还在写代码，不过比起需要考复变函数的室友，我还是很幸福的啊～
在网络接受消息的时候，字符串会有改变，并不是原来想要表达的字符串。
QWidget并没有exec_方法，现在改，使用QDialog！
QTextEdit没办法多线程实时刷新，最后使用的QTimer方法来进行替代，通过定时来使得消息进行刷新与读取，同时需要在进行消息读取的时候，对于消息队列进行上锁处理。

未完成：


- [ ] 使用skey算法来存储用户使用的密码
- [x] 各个界面的连接
- [ ] 界面中函数的调用与动作的调整
- [x] 协议调整，重新定义服务器与客户端的通信协议
- [ ] 聊天信息与界面的结合
- [x] 注册信息与界面的结合
- [x] 爬虫函数的编写，网上爬取聊天头像图（捂脸逃...
- [x] 邮件函数的编写，注册成功的时候向邮箱发送邮件(需要添加附加图片的功能)
- [x] 客户与服务器的初始功能编写
- [x] 界面之中装载图片
- [x] 连接数据库



需要学习：

- [ ]pymysql插入时间

---

![我的python][1]


  [1]: https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1494998579996&di=27ad00f1bf0a3760088bb38ee3985549&imgtype=0&src=http://www.thebigdata.cn/upload/2015-07/150717160792471.png
