import scrapy


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['weather.com']
    start_urls = ['http://weather.com.cn/']

    def parse(self, response):
        return {'weather':response.css(".w_weather").get()}
