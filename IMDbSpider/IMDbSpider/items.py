# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from api.models import IMDb_Detail


class ImdbspiderItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = IMDb_Detail
