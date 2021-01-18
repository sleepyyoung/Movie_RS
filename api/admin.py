from django.contrib import admin
from api.models import IMDb_Detail, DoubanRank, Movies, Links, BrowseRecords, Rating, UserSelectTags, Tags

# Register your models here.
admin.site.register([IMDb_Detail, DoubanRank, Movies, Links, BrowseRecords, Rating, UserSelectTags, Tags])
