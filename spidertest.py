import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
from collections import deque
from multiprocessing import Pool, Manager, Queue, Lock
import hashlib


def process(url, totalCnt, visited, nameSet):
    stack = deque()  # 存放要探索的网址
    stack.append(url)
    while stack:
        try:
            url = stack.popleft()
            visited.add(url)
            response = requests.session().get(url, headers=head, timeout=TimeOut)
            soup = BeautifulSoup(response.content, 'lxml')
            webList = soup.find_all('a')
            for webText in webList:
                web_url = webText.get('href')
                if web_url and web_url not in visited:  # web_url 非空加入stack
                    stack.append(web_url)
            # 查看该页面是否有图片
            photoList = soup.find_all('img')
            for photoText in photoList:
                photoUrl = photoText.get('src')
                if 'erweima' in photoUrl:
                    continue  # 不要二维码的图片
                if 'limg' in photoUrl:
                    continue  # 不要小图
                if 'templets' in photoUrl:
                    continue  # 不要模板图
                # photoName = photoText.get('alt')
                try:
                    temp = hashlib.md5()
                    temp.update(bytes(photoUrl, encoding='utf-8'))
                    photoName = temp.hexdigest()
                    photoStoreName = photoUrl.split('uploads')[1]
                    if photoUrl and photoStoreName not in nameSet:
                        photo = requests.session().get(photoUrl, headers=head, timeout=TimeOut)
                        with open(path+str(photoName), 'wb') as newfile:  # 图片输出
                            newfile.write(photo.content)
                        nameSet.add(photoStoreName)  # 存入名称
                        if totalCnt['cnt'] % 100 == 0:
                            print('get'+' '+str(totalCnt['cnt'])+'th'+' photo')
                        totalCnt['cnt'] += 1
                except Exception as g:
                    print(g)
        except BaseException as e:
            print(e)


if __name__ == '__main__':
    url = "http://www.meizitu.com/"
    path = '/home/rouzip/chatroom-python/picture/'
    visited = set()  # 存放已经爬取过的网址
    # stack = Queue()  #存放要探索的网址
    # stack.put(url)  #初始
    nameSet = set()  # 存放已经爬取过的图片名称
    TimeOut = 5
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows; U;'
        ' Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    totalCnt = Manager().dict()
    totalCnt['cnt'] = 0
    p = Pool(8)
    # lock=Lock()
    response = requests.session().get(url, headers=head, timeout=TimeOut)
    soup = BeautifulSoup(response.content, 'lxml')
    webList = soup.find_all('a')
    for webText in webList:
        web_url = webText.get('href')
        if web_url and web_url not in visited:  # web_url 非空加入stack
            p.apply_async(process, args=(url, totalCnt, visited, nameSet))
    p.close()
    p.join()
