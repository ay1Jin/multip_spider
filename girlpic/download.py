import requests
import re
import os
from multiprocessing import Pool
from fake_useragent import UserAgent
from lxml import etree
ua = UserAgent()

def get_imglist():
    pat1='link=(.*)'
    pat2='name=(.*)_'
    fh=open('link.txt','r',encoding='utf-8')
    contents=fh.readlines()
    fh.close()
    img_list=[]
    for content in contents:
        img_msg = {
            'name': '',
            'link': ''
        }
        rst1=re.compile(pat1).findall(content)
        rst2=re.compile(pat2).findall(content)
        if len(rst1) > 0:
            img_msg['link']=rst1[0]
            img_msg['name']=rst2[0]
            img_list.append(img_msg)
    return  img_list

def run(name,link):
    headers = {"User-Agent": ua.random}
    response=requests.get(link,headers=headers).text
    page=etree.HTML(response)
    os.mkdir('./mmpic/' +name)
    # 获得所有图片的链接
    img_srcs = page.xpath('//div[@id="content-innerText"]//img/@src')
    # 保存图片'./mmpic/绅士好图/'
    for i in range(0, len(img_srcs)):
        response = requests.get(img_srcs[i], headers=headers)
        img = response.content
        with open('./mmpic/' + name + '/' + str(i) + '.jpg', 'wb') as f:
            f.write(img)
if __name__ == '__main__':
    imglist=get_imglist()
    pool=Pool(processes=128)
    for i in range(0,len(imglist)):
        pool.apply_async(run,(imglist[i]['name'],imglist[i]['link'],))
    print('start')
    pool.close()
    pool.join()
    print('stop')