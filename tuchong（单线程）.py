import os
import re
import json
import requests
import time
import urllib.parse
import random
#import traceback
import urllib

head = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
              }
print('*'*30)
print('          ψ(*｀ー´)ψ')
print('')
print(' .'*15) 
print('           图虫爬虫') 
print(' .'*15)
print('')
print('       版本号：2019.6.19')
print('           (•́へ•́╬)')

print('*'*30)

name  = 0

ask = input('是否要从上次退出的地方开始？ y/n:')
if ask == 'y':
    f = open("爬虫断点记录.txt","a")
    f.write(' ')
    f.close

    f= open("爬虫断点记录.txt","r")
    page = f.read()
    f.close
    print('检测到上次爬取到第'+str(page)+'页，将继续')
    print('务必输入上次爬取的关键词')
else:
    page = 1




def make_url(theme,page_sum):
    url = "https://tuchong.com/rest/tags/%(theme)s/posts?page=%(pagenum)s&count=20&order=weekly" % {'theme': urllib.parse.quote(theme), 'pagenum': page_sum}
    return url
#利用requests使用get方法使用链接

def get_url(url):#用requests.get 解析 url
    try:
        r = requests.get(url, headers=head, timeout=30)
        r.raise_for_status() 
        return r
    except:
        pass
        print('?????')

def cantclick (url): #解析那个不能右键的页面//注意：总页码输入过多会报错！
    
    a = requests.get(url)
    b = json.loads(a.text) 
    abc = []
    for i in b['postList']:
        abc.append(i['url'])
        # print(abc)
    return abc


def get_jpg(url):#顾名思义，获取jpg的url
    try:
        html = get_url(url)
        url_list = list(re.findall('<img id="image\d+" class="multi-photo-image" src="([a-zA-z]+://[^\s]*)" alt="">', html.text))
        return url_list
    except:
        pass

#定义下载器模块
def download(url,theme,n):
    # for i in get_jpg:
    
    # name = img['alt']+url[-4:] #图片重名命,以后再写
    global name
    name += 1#暂时先用序号代替名称，懒得写
    name2 = str(name)+str(random.randint(1, 9999999))+'.jpg' #随机命名防止重复
    download_file = os.path.join(theme,name2) #跨平台兼容 融合文件夹路径+图片名
    try:
        print("正在下载第%d套图，一共%d套图" % (n, len(cantclick_list)))
        urllib.request.urlretrieve(url,filename=download_file)
        
        print('共下载了'+str(name)+'张')
        print('---'*10)
    except:
        print('下载失败')
        pass      

if __name__ == '__main__':
    theme = input("输入你想看的类型，如 人像 人文 私房(误) 死库水(大误) 或其他：")
    page_sum = int(page)
    folder = os.getcwd()+'/'+theme # xxx = os.getcwd() #获取当前绝对路径 # + 编写目录
    test=os.path.exists(folder)
    if not test:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.mkdir(folder)            #--------------------创建theme文件夹
    
            print('初始化...')
            
    else:
            # 如果目录存在则不创建，并提示目录已存在
            print('初始化完成...')
   
    m = 0
    while True:
        n = 0
        m += 1
        page_sum += 1
        print("正在下载第%d页，共%d页" % (m, page_sum))
        f = open("爬虫断点记录.txt","w")
        f.write(str(page_sum))
        print('进度已储存')
        f.close
        url = make_url(theme,page_sum)
        
        cantclick_list = cantclick(url)
        if len(cantclick_list) == 0:
            print('爬取结束') 
            break

        
        for ii in cantclick_list:
            jpg_list = get_jpg(ii)
            n += 1
            for iii in jpg_list:
                jpg = iii
                download(jpg,theme,n)
                # time.sleep(random.randint(1, 4))  #防反爬，视情况调整
                

