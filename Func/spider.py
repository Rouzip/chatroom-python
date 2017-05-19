import requests
import hashlib
from bs4 import BeautifulSoup
from collections import deque
import logging
import os

def pictureSpider(url, visited, nameSet):
    # 存放要遍历的网站
    stack = deque()
    stack.append(url)
    while stack:
        try:
            picUrl = stack.popleft()
            visited.add(picUrl)
            response = requests.session().get(
                picUrl, headers=head, timeout=Timeout)
            bsp = BeautifulSoup(response.content, 'lxml')
            webList = bsp.find_all('a')
            for webText in webList:
                webUrl = webText.get('href')
                # BFS 遍历，将本页链接全部加入到已浏览
                if webUrl and webUrl not in visited:
                    stack.append(webUrl)

            photoList = bsp.find_all('img')
            for photoText in photoList:
                photoUrl = photoText.get('src')
                if 'erweima' in photoUrl:
                    continue  # 不要二维码的图片
                if 'limg' in photoUrl:
                    continue  # 不要小图
                if 'templets' in photoUrl:
                    continue  # 不要模板图
                try:
                    # 使用md5函数对名字进行缩略
                    temp = hashlib.md5()
                    temp.update(bytes(photoUrl, encoding='utf-8'))
                    photoName = temp.hexdigest()
                    if photoUrl and photoName not in nameSet:
                        photo = requests.session().get(
                            photoUrl, headers=head, timeout=Timeout)
                        with open(path + photoName + '.jpg', 'wb') as fp:
                            fp.write(photo.content)
                        nameSet.add(photoName)
                    pictureNum = os.listdir(
                        '/home/rouzip/chatroom-python/picture')
                    if len(pictureNum) >= 30:
                        return
                except Exception as g:
                    logging.exception(g)
        except Exception as e:
            logging.exception(e)


# 存放访问的设定
# head 和　超时时间
head = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64)'
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
Timeout = 5


# 存储地址　初始URL
url = "http://www.meizitu.com/"
path = '/home/rouzip/chatroom-python/picture/'


nameSet = set()
visited = set()


if __name__ == '__main__':
    pictureSpider(url, visited, nameSet)
