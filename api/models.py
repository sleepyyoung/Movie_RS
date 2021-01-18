from django.db import models
from enter.models import UserInfo


class IMDb_Detail(models.Model):
    imdbid = models.CharField(max_length=100, verbose_name="imdbid")
    imdb_link = models.CharField(max_length=100, verbose_name="IMDb链接")
    picture_link = models.CharField(max_length=500, verbose_name="图片链接")
    title = models.CharField(max_length=100, verbose_name="名称")
    year = models.CharField(max_length=100, verbose_name="年份")
    score = models.CharField(max_length=100, verbose_name="评分")
    rating_count = models.CharField(max_length=100, verbose_name="评分人数")
    length = models.CharField(max_length=100, verbose_name="时长")
    the_type = models.CharField(max_length=100, verbose_name="类型")
    premiere = models.CharField(max_length=100, verbose_name="首映")
    summary = models.CharField(max_length=500, verbose_name="摘要")
    director = models.CharField(max_length=100, verbose_name="导演")
    writers = models.CharField(max_length=100, verbose_name="作者")
    stars = models.CharField(max_length=100, verbose_name="演员")
    story_line = models.TextField(verbose_name="故事情节")
    did_you_know = models.TextField(verbose_name="你知道吗")

    class Meta:
        verbose_name = "IMDb电影详情"
        verbose_name_plural = verbose_name


class DoubanRank(models.Model):
    srank = models.IntegerField(verbose_name="排名")
    href = models.CharField(max_length=500, verbose_name="链接")
    director = models.CharField(max_length=500, verbose_name="导演")
    screenwriter = models.CharField(max_length=500, verbose_name="编剧")
    actor = models.TextField(verbose_name="主演")
    type = models.CharField(max_length=500, verbose_name="类型")
    country = models.CharField(max_length=500, verbose_name="制片国家")
    language = models.CharField(max_length=100, verbose_name="语言")
    release_time = models.CharField(max_length=100, verbose_name="上映时间")
    duration = models.CharField(max_length=100, verbose_name="片长")
    nickname = models.TextField(verbose_name="又名")
    imdb_link = models.CharField(max_length=100, verbose_name="imdb链接")
    img_href = models.CharField(max_length=500, verbose_name="图片链接")
    title = models.CharField(max_length=500, verbose_name="电影名称")
    score = models.CharField(max_length=500, verbose_name="评分")
    evaluator = models.CharField(max_length=500, verbose_name="评价人数")

    class Meta:
        verbose_name = "豆瓣电影排行榜"
        verbose_name_plural = verbose_name


#
# class BrowseRecords(models.Model):
#     # id = models.AutoField(db_column='Id', primary_key=True)
#     username = models.ForeignKey(UserInfo, models.DO_NOTHING, db_column='username')
#     imdbid = models.IntegerField(blank=True, null=True, verbose_name="imdbid")
#     time = models.DateTimeField(blank=True, null=True, verbose_name="时间")
#
#     class Meta:
#         managed = True
#         verbose_name = "足迹（浏览记录）"
#         verbose_name_plural = verbose_name
#
#
# class Movies(models.Model):
#     movieid = models.IntegerField(unique=True, blank=True, null=True, verbose_name="电影ID")
#     # title = models.CharField(max_length=255, blank=True, null=True, verbose_name="电影名称")
#     genres = models.CharField(max_length=255, blank=True, null=True, verbose_name="电影类型")
#
#     class Meta:
#         db_table = 'movies'
#         managed = True
#         verbose_name = "电影数据集"
#         verbose_name_plural = verbose_name
#
#
# class Links(models.Model):
#     # id = models.AutoField(db_column='Id', primary_key=True)
#     movieid = models.ForeignKey('Movies', models.DO_NOTHING, db_column='movieId', blank=True, null=True,
#                                 verbose_name="movieid")
#     imdbid = models.IntegerField(verbose_name="imdbid", max_length=100, blank=True,
#                                  null=True)
#
#     class Meta:
#         db_table = 'links'
#         managed = True
#         verbose_name = "电影外链"
#         verbose_name_plural = verbose_name
#
#
# class Ratings(models.Model):
#     # id = models.AutoField(db_column='Id', primary_key=True)
#     userid = models.ForeignKey(UserInfo, models.DO_NOTHING, blank=True, null=True, verbose_name="UserId")
#     movieid = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True, verbose_name="MovieId")
#     rating = models.FloatField(blank=True, null=True, verbose_name="评分")
#
#     class Meta:
#         db_table = 'ratings'
#         managed = True
#         verbose_name = "用户对电影的评分"
#         verbose_name_plural = verbose_name
#
#
# class Tags(models.Model):
#     # id = models.AutoField(primary_key=True)
#     userid = models.IntegerField(verbose_name="UserId")
#     tagid = models.CharField(max_length=250, verbose_name="TagId")
#
#     class Meta:
#         managed = True
#         verbose_name = "用户选择的电影标签"
#         verbose_name_plural = verbose_name

class Movies(models.Model):
    movieid = models.CharField(max_length=100, verbose_name="电影ID")
    # title = models.CharField(max_length=100, verbose_name="电影名称", null=True)
    genres = models.CharField(max_length=100, verbose_name="电影类型")

    class Meta:
        verbose_name = "电影数据集"
        verbose_name_plural = verbose_name


class Links(models.Model):
    imdbid = models.CharField(max_length=100, verbose_name="imdbid")
    movieid = models.CharField(max_length=100, verbose_name="电影ID")

    class Meta:
        verbose_name = "电影外链"
        verbose_name_plural = verbose_name


class BrowseRecords(models.Model):
    username = models.CharField(max_length=100, verbose_name="username")
    userid = models.CharField(max_length=100, verbose_name="userid")
    imdbid = models.CharField(max_length=100, verbose_name="imdbid")
    movieid = models.CharField(max_length=100, verbose_name="movieid")
    time = models.DateTimeField(verbose_name="时间")

    class Meta:
        verbose_name = "足迹（浏览记录）"
        verbose_name_plural = verbose_name


class Rating(models.Model):
    userid = models.CharField(max_length=100, verbose_name="UserId")
    movieid = models.CharField(max_length=100, verbose_name="MovieId")
    rating = models.CharField(max_length=100, verbose_name="评分")

    class Meta:
        verbose_name = "用户对电影的评分"
        verbose_name_plural = verbose_name


class UserSelectTags(models.Model):
    userid = models.CharField(max_length=100, verbose_name="UserId")
    tagid = models.CharField(max_length=100, verbose_name="TagId")

    class Meta:
        verbose_name = "用户选择的电影标签"  # 用户注册时候选择的
        verbose_name_plural = verbose_name


class Tags(models.Model):
    tagid = models.CharField(max_length=100, verbose_name="TagId")
    tagname = models.CharField(max_length=100, verbose_name="TagName")

    class Meta:
        verbose_name = "TagId--TagName"
        verbose_name_plural = verbose_name


class Relevance(models.Model):
    movieid = models.CharField(max_length=100, verbose_name="movieid")
    tagid = models.CharField(max_length=100, verbose_name="TagId")
    relevance = models.CharField(max_length=100, verbose_name="TagName")

    class Meta:
        verbose_name = "MovieId与TagId的相关性"  # 已处理 Relevance > 0.9
        verbose_name_plural = verbose_name
