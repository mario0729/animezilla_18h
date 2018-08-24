# -*- coding: utf-8 -*-
import scrapy
import requests
from animezilla_18h.items import Animezilla18HItem

class Spider18hSpider(scrapy.Spider):
    name = 'Spider_18h'
    allowed_domains = ['18h.animezilla.com']
    start_urls = ['https://18h.animezilla.com/manga/3429']
    for i in range(1,1000):
        url = 'https://18h.animezilla.com/manga/'+str(i)
        start_urls.append(url)

    def parse(self, response):
        if response.status == 200:
            url = response.url
            yield scrapy.Request(url=url,callback=self.parse_url)    
            f = open(r'D:\Spider_download\animezilla_18h_images\1.txt', 'a+')
            f.write(url)
            f.write('\n')
            f.close()
        else:
            print('%s不存在!!!!'%url)

    def parse_url(self, response):
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
            url = 'https://18h.animezilla.com/manga/3429/'+str(i)
            yield scrapy.Request(url = url,callback=self.parse_image,meta={'comicname':comicname,'page':i})
            i+=1

    def parse_image(self, response):
        item = Animezilla18HItem()
        item['image_urls'] = [response.css('#page-current img::attr(src)').extract_first()]
        item['image_name'] = response.meta['comicname']
        item['page'] = response.meta['page']
        item['url'] = response.url
        #print(item['image_name']+item['image_urls'])
        yield item
        