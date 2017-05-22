# chatroom-python
my test for computer network

---

系统环境：Ubuntu16.04
数据库：mysql Ver 14.14 Distrib 5.7.18, for Linux (x86_64)
相关包依赖：
pyqt5
concurrent.futures
requests
BeautifulSoup
python版本：python3.5.2

---

## **开发目的**
本程序开发目的是在可能被监听信道上建立安全的c/s通信。

---

## **使用手册**
可在任意目录下开启终端，输入“python server.py”，开启服务器。
在客户端目录下输入“python clientMain.py”开启服务器（同时需要保证子模块clientFunc，clientChat，clientSignup在同一目录下）。
在客户端注册栏中输入自己的相关信息，从所填写的邮箱之中取出hash密码文件存放在客户端的相同目录下，输入密码即可以登录聊天系统。使用[<name>]:<message>格式发送消息（all为群发）。

---

![我的python][1]


  [1]: https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1494998579996&di=27ad00f1bf0a3760088bb38ee3985549&imgtype=0&src=http://www.thebigdata.cn/upload/2015-07/150717160792471.png
