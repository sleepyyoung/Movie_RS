# Generated by Django 3.1.2 on 2021-01-12 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrowseRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='username')),
                ('userid', models.CharField(max_length=100, verbose_name='userid')),
                ('imdbid', models.CharField(max_length=100, verbose_name='imdbid')),
                ('movieid', models.CharField(max_length=100, verbose_name='movieid')),
                ('time', models.DateTimeField(verbose_name='时间')),
            ],
            options={
                'verbose_name': '足迹（浏览记录）',
                'verbose_name_plural': '足迹（浏览记录）',
            },
        ),
        migrations.CreateModel(
            name='DoubanRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srank', models.IntegerField(verbose_name='排名')),
                ('href', models.CharField(max_length=500, verbose_name='链接')),
                ('director', models.CharField(max_length=500, verbose_name='导演')),
                ('screenwriter', models.CharField(max_length=500, verbose_name='编剧')),
                ('actor', models.CharField(max_length=500, verbose_name='主演')),
                ('type', models.CharField(max_length=500, verbose_name='类型')),
                ('country', models.CharField(max_length=500, verbose_name='制片国家')),
                ('language', models.CharField(max_length=100, verbose_name='语言')),
                ('release_time', models.CharField(max_length=100, verbose_name='上映时间')),
                ('duration', models.CharField(max_length=100, verbose_name='片长')),
                ('nickname', models.CharField(max_length=100, verbose_name='又名')),
                ('imdb_link', models.CharField(max_length=100, verbose_name='imdb链接')),
                ('img_href', models.CharField(max_length=500, verbose_name='图片链接')),
                ('title', models.CharField(max_length=500, verbose_name='电影名称')),
                ('score', models.FloatField(verbose_name='评分')),
                ('evaluator', models.IntegerField(verbose_name='评价人数')),
            ],
            options={
                'verbose_name': '豆瓣电影排行榜',
                'verbose_name_plural': '豆瓣电影排行榜',
            },
        ),
        migrations.CreateModel(
            name='IMDb_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdbid', models.CharField(max_length=100, verbose_name='imdbid')),
                ('imdb_link', models.CharField(max_length=100, verbose_name='IMDb链接')),
                ('picture_link', models.CharField(max_length=500, verbose_name='图片链接')),
                ('title', models.CharField(max_length=100, verbose_name='名称')),
                ('year', models.CharField(max_length=100, verbose_name='年份')),
                ('score', models.CharField(max_length=100, verbose_name='评分')),
                ('rating_count', models.CharField(max_length=100, verbose_name='评分人数')),
                ('length', models.CharField(max_length=100, verbose_name='时长')),
                ('the_type', models.CharField(max_length=100, verbose_name='类型')),
                ('premiere', models.CharField(max_length=100, verbose_name='首映')),
                ('summary', models.CharField(max_length=500, verbose_name='摘要')),
                ('director', models.CharField(max_length=100, verbose_name='导演')),
                ('writers', models.CharField(max_length=100, verbose_name='作者')),
                ('stars', models.CharField(max_length=100, verbose_name='演员')),
                ('story_line', models.TextField(verbose_name='故事情节')),
                ('did_you_know', models.TextField(verbose_name='你知道吗')),
            ],
            options={
                'verbose_name': 'IMDb电影详情',
                'verbose_name_plural': 'IMDb电影详情',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdbid', models.CharField(max_length=100, verbose_name='imdbid')),
                ('movieid', models.CharField(max_length=100, verbose_name='电影ID')),
            ],
            options={
                'verbose_name': '电影外链',
                'verbose_name_plural': '电影外链',
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieid', models.CharField(max_length=100, verbose_name='电影ID')),
                ('genres', models.CharField(max_length=100, verbose_name='电影类型')),
            ],
            options={
                'verbose_name': '电影数据集',
                'verbose_name_plural': '电影数据集',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100, verbose_name='UserId')),
                ('movieid', models.CharField(max_length=100, verbose_name='MovieId')),
                ('rating', models.CharField(max_length=100, verbose_name='评分')),
            ],
            options={
                'verbose_name': '用户对电影的评分',
                'verbose_name_plural': '用户对电影的评分',
            },
        ),
        migrations.CreateModel(
            name='Relevance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movieid', models.CharField(max_length=100, verbose_name='movieid')),
                ('tagid', models.CharField(max_length=100, verbose_name='TagId')),
                ('relevance', models.CharField(max_length=100, verbose_name='TagName')),
            ],
            options={
                'verbose_name': 'MovieId与TagId的相关性',
                'verbose_name_plural': 'MovieId与TagId的相关性',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagid', models.CharField(max_length=100, verbose_name='TagId')),
                ('tagname', models.CharField(max_length=100, verbose_name='TagName')),
            ],
            options={
                'verbose_name': 'TagId--TagName',
                'verbose_name_plural': 'TagId--TagName',
            },
        ),
        migrations.CreateModel(
            name='UserSelectTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100, verbose_name='UserId')),
                ('tagid', models.CharField(max_length=100, verbose_name='TagId')),
            ],
            options={
                'verbose_name': '用户选择的电影标签',
                'verbose_name_plural': '用户选择的电影标签',
            },
        ),
    ]
