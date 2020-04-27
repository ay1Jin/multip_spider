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
## 创建名字
for i in range(0,len(class_names)):
    try:
        n = class_names[i]
        class_name = n.find_element_by_xpath('.//span').text
        os.mkdir('./mmpic/'+class_name)
        print(class_name)
        # 进入该分区
        n.find_element_by_xpath('.//span').click()
        #获得该分区的总页数
        pages=browser.find_elements_by_xpath('//div[@class="btn-group fl"]//button')
        page=pages[-1].text
        print(page)
        page = int(page)
        for p in range(0, page):
            try:
                # 获得当前页面的图片链接
                browser.refresh()
                sleep(1)
                all_h2 = browser.find_elements_by_xpath('//div[@class="grid-bor"]//h2/a')
                for msg in all_h2:
                    try:
                        name = msg.text
                        link = msg.get_attribute('href')
                        print(name + link)
                        url = link
                        dirname = name
                        os.mkdir('./mmpic/'+ class_name +'/'+ dirname)
                        page2 = requests.get(url, headers=User_Agent).text
                        source2 = etree.HTML(page2)
                        # 获得所有图片的链接
                        img_srcs = source2.xpath('//div[@id="content-innerText"]//img/@src')
                        # 保存图片
                        for i in range(0, len(img_srcs)):
                            response = requests.get(img_srcs[i], headers=User_Agent)
                            img = response.content
                            with open('./mmpic/'+ class_name +'/'+ dirname + '/' + str(i) + '.jpg', 'wb') as f:
                                f.write(img)
                    except:
                        continue
                print('第%d已经完成' % p)
                browser.find_element_by_xpath('//button[@class="empty navbtr"]').click()
            except:
                continue
        print('Done!')
        browser.back()
        sleep(1)
        class_names=browser.find_elements_by_xpath('//ul[@class="l-8"]//a[@class="pos-a"]')
    except:
        print('出现异常')
        continue
