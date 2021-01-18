# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import ssl
import urllib
from urllib import request


class ImdbspiderPipeline:
    def __init__(self):
        self.images_path = "../static/IMDb_imgs/"

    def process_item(self, item, spider):
        image_url = item["picture_link"]
        image_name = item["imdbid"] + ".jpg"
        try:
            request.urlretrieve(image_url, os.path.join(self.images_path, image_name))
        except ValueError as e:
            print(e)
        except ssl.SSLError as e:
            print(e)
        except Exception as e:
            print(e)
        item.save()
