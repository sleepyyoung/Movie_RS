# Generated by Django 3.1.2 on 2021-01-13 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210113_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doubanrank',
            name='nickname',
            field=models.TextField(verbose_name='又名'),
        ),
    ]
