# Generated by Django 3.1.2 on 2021-01-13 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0002_auto_20210112_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpasswordcaptcha',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 10, 45, 48), verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='registercaptcha',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 10, 45, 48), verbose_name='过期时间'),
        ),
    ]
