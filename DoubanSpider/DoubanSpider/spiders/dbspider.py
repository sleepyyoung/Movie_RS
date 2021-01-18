import scrapy
from DoubanSpider.items import DoubanspiderItem


class DbspiderSpider(scrapy.Spider):
    name = 'dbspider'
    allowed_domains = ['movie.douban.com']
    start_urls = [f"https://movie.douban.com/top250?start={i}" for i in range(0, 250, 25)]

    def parse(self, response):
        for res in response.xpath('//ol[@class="grid_view"]/li'):
            href = res.xpath('div/div[1]/a/@href').extract_first()
            yield scrapy.Request(
                url=href,
                callback=self.parse_detail,
            )

    def parse_detail(self, response):
        item = DoubanspiderItem()
        srank = response.xpath("//*[@id=\"content\"]/div[1]/span[1]/text()").extract_first()[3:]
        href = response.url
        info = "".join(response.xpath("//*[@id=\"info\"]//text()").extract()).replace(" ", "").split("\n")[1:-2]
        del info[4]
        director = info[0]
        screenwriter = info[1]
        actor = info[2]
        type = info[3]
        country = info[4]
        language = info[5]
        release_time = info[6]
        duration = info[7]
        nickname = info[8]
        imdb_link = info[9][7:]
        img_href = response.xpath("//*[@id=\"mainpic\"]/a/img/@src").extract_first()
        score = response.xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/strong/text()").extract_first()
        evaluator = response.xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/div/div[2]/a/span/text()").extract_first()
        title = response.xpath("//*[@id=\"content\"]/h1/span[1]/text()").extract_first() + "  " + response.xpath(
            "//*[@id=\"content\"]/h1/span[2]/text()").extract_first()

        item["srank"] = int(srank)
        item["href"] = href
        item["director"] = director
        item["screenwriter"] = screenwriter
        item["actor"] = actor
        item["type"] = type
        item["country"] = country
        item["language"] = language
        item["release_time"] = release_time
        item["duration"] = duration
        item["nickname"] = nickname
        item["imdb_link"] = imdb_link
        item["img_href"] = img_href
        item["title"] = title
        item["score"] = float(score)
        item["evaluator"] = int(evaluator)

        yield item
