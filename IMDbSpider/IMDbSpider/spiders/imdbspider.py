import json
import random
import scrapy
from IMDbSpider.items import ImdbspiderItem
from django.core import serializers

from api.models import Links
import re
from home import models
from api.models import IMDb_Detail


class ImdbspiderSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    result = Links.objects.values("imdbid")
    start_urls = ["https://www.imdb.com/title/tt00" + _["imdbid"] for _ in list(result)]

    def parse(self, response):
        item = ImdbspiderItem()
        imdbid = response.url.split("/")[-2][2:]
        imdb_history = len(json.loads(serializers.serialize("json", IMDb_Detail.objects.filter(imdbid=imdbid))))
        if imdb_history == 0:
            imdb_link = response.url
            picture_link = str(response.xpath(
                "//*[@id=\"title-overview-widget\"]//div[@class=\"poster\"]/a/img/@src").extract_first())
            title = str(response.xpath(
                "//*[@id=\"title-overview-widget\"]//div[@class=\"title_wrapper\"]/h1/text()").extract_first()).replace(
                "\xa0", "")
            year = str(response.xpath(
                "//*[@id=\"title-overview-widget\"]//div[@class=\"title_wrapper\"]/h1/span[@id=\"titleYear\"]/a/text()").extract_first(
            )).replace("\xa0", "")
            score = str(response.xpath(
                "//*[@id=\"title-overview-widget\"]//div[@class=\"ratingValue\"]/strong/span/text()").extract_first())
            rating_count = str(response.xpath(
                "//*[@id=\"title-overview-widget\"]//a/span[@class=\"small\"]/text()").extract_first()).replace(",", "")
            try:
                subtext = "".join(response.xpath(
                    "string(//*[@id=\"title-overview-widget\"]//div[@class=\"subtext\"])").extract()).replace(
                    "\n", "").split("|")[1:]
                length, the_type, premiere = subtext[0].strip(), subtext[1].replace(" ", ""), subtext[2].strip()
            except IndexError:
                subtext = "".join(response.xpath(
                    "string(//*[@id=\"title-overview-widget\"]//div[@class=\"subtext\"])").extract()).replace(
                    "\n", "").split("|")
                try:
                    length, the_type, premiere = subtext[0].strip(), subtext[1].replace(" ", ""), subtext[2].strip()
                except IndexError:
                    length, the_type, premiere = "", "", ""
            story_line = str(
                response.xpath(
                    "string(//*[@id=\"titleStoryLine\"]/div[@class=\"inline canwrap\"]/p/span)").extract_first())
            did_you_know = str(
                response.xpath("string(//*[@id=\"trivia\"])").extract_first()).replace("Trivia", "")
            try:
                did_you_know = re.findall(r"(.*?)See.*?", did_you_know, re.S)[0].strip()
            except IndexError:
                did_you_know = ""

            summary = str(response.xpath(
                "string(//*[@id=\"title-overview-widget\"]//div[@class=\"summary_text\"])").extract_first(
            )).replace("\n", "").strip()
            director = ""
            writers = ""
            stars = ""
            credit_summary = response.xpath(
                "//*[@id=\"title-overview-widget\"]//div[@class=\"plot_summary \"]/div[@class=\"credit_summary_item\"]")
            if len(credit_summary) == 3:
                director = credit_summary[0].xpath("*//text()").extract()[-1]
                writers = credit_summary[1].xpath("*//text()").extract()
                writers = ",".join(writers[1:-2] if writers[-2] == "|" else writers)
                stars = credit_summary[2].xpath("*//text()").extract()
                stars = stars[-1] if len(stars) == 2 else ",".join(stars[1:-2] if stars[-2] == "|" else stars)
            if len(credit_summary) == 2:
                director = credit_summary[0].xpath("*//text()").extract()[-1]
                stars = credit_summary[1].xpath("*//text()").extract()
                stars = stars[-1] if len(stars) == 2 else ",".join(stars[1:-2] if stars[-2] == "|" else stars)
            if len(credit_summary) == 1:
                director = credit_summary[0].xpath("*//text()").extract()[-1]

            item["imdbid"] = imdbid
            item["imdb_link"] = imdb_link
            item["picture_link"] = picture_link
            item["title"] = title
            item["year"] = year
            item["score"] = score
            item["rating_count"] = rating_count
            item["length"] = length
            item["the_type"] = the_type
            item["premiere"] = premiere
            item["summary"] = summary
            item["director"] = director
            item["writers"] = writers
            item["stars"] = stars
            item["story_line"] = story_line
            item["did_you_know"] = did_you_know
            print(item["imdbid"])
            yield item
        else:
            print(imdbid, "已存在，跳过")
