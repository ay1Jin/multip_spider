from urllib import request
from lxml import etree
import re
import requests
from multiprocessing import Pool
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
def get_allpage(url):
    page=requests.get(url,headers=headers).text
    page_element=etree.HTML(page)
    sum_page=page_element.xpath('//div[@class="navigation container"]//a[@class="extend"]/@href')[0]
    print(sum_page)
    pat='/page/(.*)'
    rst=re.compile(pat).findall(sum_page)[0]
    return int(rst)

def get_img(url):
    page = requests.get(url, headers=headers).text
    page_element = etree.HTML(page)
    img_link = page_element.xpath('//a[@class="zoom"]//img/@src')
    img_name = page_element.xpath('//a[@class="zoom"]//img/@alt')
    for i in range(0,len(img_link)):
        filename=img_name[i]
        request.urlretrieve(img_link[i],filename=filename+'.png')
    print('链接：%s 已经完成' %url)

if __name__ == '__main__':
    start_url='http://www.obzhi.com/page/1'
    sum_page=get_allpage(start_url)
    print('全站共%d个页面' %sum_page)
    p=Pool(10)
    for i in range(1,sum_page+1):
        url = 'http://www.obzhi.com/page/'+str(i)
        p.apply_async(get_img,(url,))
    p.close()
    p.join()
    print('全部完成')
