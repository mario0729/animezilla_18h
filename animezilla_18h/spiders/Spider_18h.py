# -*- coding: utf-8 -*-
import scrapy
import requests
from animezilla_18h.items import Animezilla18HItem

class Spider18hSpider(scrapy.Spider):
    name = 'Spider_18h'
    allowed_domains = ['18h.animezilla.com']
    start_urls = []
    #for url in open(r'D:\Spider_download\animezilla_18h_images\1.txt'): 
        #url = "'"+url.strip()+"'"
        #print(url) 
        #start_urls.append(url)
    for i in range(80,100):
        url = 'https://18h.animezilla.com/manga/'+str(i)
        r = requests.get(url)
        if r.status_code == 200:
            print('%s yes!!!'%url)
            start_urls.append(url)

    def parse(self, response):
        #comicname表示漫画名字
        #page 表示当前页数
        #page_num表示漫画总页数
        a = response.css('.entry-header h1::text').extract_first()
        b = a.split(' ')
        c = len(b)
        comicname = ''
        for i in range(0,c-2):
            comicname = comicname + b[i]
        pageinfo = b[c-1]
        page = pageinfo.split('/')[0]
        page_num = pageinfo.split('/')[1]
        print(comicname)

        i = 1
        while i <= int(page_num):
            url = response.url+'/'+str(i)
            yield scrapy.Request(url = url,callback=self.parse_image,meta={'comicname':comicname,'page':i})
            i+=1

    def parse_image(self, response):
        item = Animezilla18HItem()
        item['image_urls'] = [response.css('.entry-content p img::attr(src)').extract_first()]
        item['image_name'] = response.meta['comicname']
        item['page'] = response.meta['page']
        item['url'] = response.url
        #print(item['image_name']+item['image_urls'])
        yield item
        