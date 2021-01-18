from django.contrib import admin
from enter.models import UserInfo, RegisterCaptcha, ForgotPasswordCaptcha

# Register your models here.
admin.site.register([UserInfo, RegisterCaptcha, ForgotPasswordCaptcha])
