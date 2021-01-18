# Generated by Django 3.1.2 on 2021-01-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210113_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubanrank',
            name='evaluator',
            field=models.CharField(max_length=500, verbose_name='评价人数'),
        ),
        migrations.AlterField(
            model_name='doubanrank',
            name='score',
            field=models.CharField(max_length=500, verbose_name='评分'),
        ),
        migrations.AlterField(
            model_name='doubanrank',
            name='srank',
            field=models.CharField(max_length=500, verbose_name='排名'),
        ),
    ]
