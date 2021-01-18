import datetime

from captcha.fields import CaptchaField
from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    nickname = models.CharField(max_length=11, unique=False, null=True, verbose_name="昵称")

    # Adventure = models.CharField(max_length=11, null=True, verbose_name="冒险")
    # Animation = models.CharField(max_length=11, null=True, verbose_name="动画")
    # Children = models.CharField(max_length=11, null=True, verbose_name="儿童")
    # Comedy = models.CharField(max_length=11, null=True, verbose_name="喜剧")
    # Fantasy = models.CharField(max_length=11, null=True, verbose_name="幻想")
    # Romance = models.CharField(max_length=11, null=True, verbose_name="爱情")
    # Action = models.CharField(max_length=11, null=True, verbose_name="动作")
    # Crime = models.CharField(max_length=11, null=True, verbose_name="犯罪")
    # Thriller = models.CharField(max_length=11, null=True, verbose_name="惊悚")
    # FilmNoir = models.CharField(max_length=11, null=True, verbose_name="暗黑")
    # Horror = models.CharField(max_length=11, null=True, verbose_name="恐怖")
    # Drama = models.CharField(max_length=11, null=True, verbose_name="戏剧")
    # Mystery = models.CharField(max_length=11, null=True, verbose_name="神秘")
    # SciFi = models.CharField(max_length=11, null=True, verbose_name="科幻")
    # War = models.CharField(max_length=11, null=True, verbose_name="战争")
    # Western = models.CharField(max_length=11, null=True, verbose_name="西部")
    # Musical = models.CharField(max_length=11, null=True, verbose_name="音乐")
    # IMAX = models.CharField(max_length=11, null=True, verbose_name="IMAX")
    # Others = models.CharField(max_length=11, null=True, verbose_name="其它")

    class Meta:
        verbose_name = "用户"  # 继承自Django自带的用户模块
        verbose_name_plural = verbose_name


# 注册验证码
class RegisterCaptcha(models.Model):
    captcha = models.CharField(max_length=6, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    deadline = models.DateTimeField(verbose_name="过期时间", default=datetime.datetime.strptime(
        (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S"))  # 当前时间 5分钟后(验证码有效期为5分钟)

    class Meta:
        verbose_name = "注册验证码"
        verbose_name_plural = verbose_name


# 忘记密码验证码
class ForgotPasswordCaptcha(models.Model):
    captcha = models.CharField(max_length=6, verbose_name="验证码")
    email = models.EmailField(verbose_name="邮箱")
    deadline = models.DateTimeField(verbose_name="过期时间", default=datetime.datetime.strptime(
        (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S"))  # 当前时间 5分钟后(验证码有效期为5分钟)

    class Meta:
        verbose_name = "忘记密码验证码"
        verbose_name_plural = verbose_name
