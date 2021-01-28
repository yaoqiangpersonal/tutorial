import scrapy
import re

from tutorial.items import BuyoyoItem

class BuyoyoSpider(scrapy.Spider):
    name = 'buyoyo'
    allowed_domains = ['buyoyo.com']
    start_urls = ['http://buyoyo.com/biz/mainPage.do']

    def start_requests(self):
        data = {
            'username': '3112914015',
            'password': 'zhang123456'
        }
        yield scrapy.FormRequest(
            url="https://www.buyoyo.com/biz/Login.do",
            formdata=data,
            callback=self.after_login
        )

    # 登录成功之后操作

    def after_login(self, response):
        cookie1 = response.headers.getlist('Set-Cookie')
        def flat_map(f, xs): 
            return [y for ys in xs for y in f(ys)]

        dic = {i[0]: i[1] for i in map(lambda a: a.split('='),
                                       filter(lambda s: s.count('=') > 0,
                                              flat_map(lambda s: s.split(";"),
                                                       map(lambda o: o.decode('UTF-8'), cookie1))
                                              )
                                       )}
        for page in range(1,4):
            yield scrapy.Request(
            url="https://www.buyoyo.com/biz/GlobalSearch.do?keyword=&KEYOPTION=Vname&ProductType=0&ProductType2=56&gsPageNo=" + str(page),
            callback=self.parse,
            cookies=dic,
            meta={'cookie': dic})

    def parse(self, response):

        for a in response.css('.videoBorder tr'):
            tdlist = a.css('td').getall()
            if(len(tdlist) >= 3):
                print(a.xpath('//b[contains(text(),"HK$")]/text()').get())
                yield BuyoyoItem(id=a.css('.black::attr(href)').re_first(r'\d{6,}'),name=a.css('.black>b::text').get(), price= a.xpath('//b[contains(text(),"HK$")]/text()').get())
        return None
