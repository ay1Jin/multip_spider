from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
import requests
from lxml import etree
req_url = "https://www.jdlingyu.mobi/collections"
User_Agent={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}
browser=webdriver.Chrome()
browser.get(req_url)
name_lis=[]
class_names=browser.find_elements_by_xpath('//ul[@class="l-8"]//a[@class="pos-a"]')
## 创建分类
fh = open('link.txt','a+',encoding='utf-8')
for i in range(0,len(class_names)):
    class_names = browser.find_elements_by_xpath('//ul[@class="l-8"]//a[@class="pos-a"]')
    n = class_names[i]
    class_name = n.find_element_by_xpath('.//span').text
    #os.mkdir('./mmpic/'+class_name)
    print(class_name)
    fh.write('主题:'+class_name+'\n')
    # 进入该分区
    n.find_element_by_xpath('.//span').click()
    # 获得该分区的总页数
    pages = browser.find_elements_by_xpath('//div[@class="btn-group fl"]//button')
    page = pages[-1].text
    print(page)
    page = int(page)
    for p in range(0,page):
        try:
            all_h2 = browser.find_elements_by_xpath('//div[@class="grid-bor"]//h2/a')
            for msg in all_h2:
                try:
                    name = msg.text
                    link = msg.get_attribute('href')
                    allmsg = 'name='+name+'_link='+link
                    print(allmsg)
                    fh.write(allmsg+'\n')
                except:
                    print('异常')
        except:
            continue
        browser.find_element_by_xpath('//button[@class="empty navbtr"]').click()
        sleep(0.5)
    sleep(1)
    browser.back()
    sleep(5)
fh.close()