from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
import requests
from lxml import etree
req_url = "https://www.jdlingyu.mobi/collection/meizitu"
User_Agent={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}
browser=webdriver.Chrome()
browser.get(req_url)
# 获得该分区的总页数
pages = browser.find_elements_by_xpath('//div[@class="btn-group fl"]//button')
page = pages[-1].text
print(page)
page = int(page)
fh = open('link.txt','a+',encoding='utf-8')
for p in range(0, page):
    try:
        sleep(0.8)
        all_h2 = browser.find_elements_by_xpath('//div[@class="grid-bor"]//h2/a')
        for msg in all_h2:
            try:
                name = msg.text
                link = msg.get_attribute('href')
                allmsg = 'name=' + name + '_link=' + link
                print(allmsg)
                fh.write(allmsg + '\n')
            except:
                print('异常')
        browser.find_element_by_xpath('//button[@class="empty navbtr"]').click()
    except:
        continue
fh.close()