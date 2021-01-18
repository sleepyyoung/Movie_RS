import datetime
import json
import random
from django.forms import model_to_dict
from rest_framework.views import APIView
import django
from django.core import serializers
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from enter import models
from api.models import Tags, UserSelectTags
from django.contrib.auth import authenticate, login, logout
from enter.forms import LoginForm, RegisterForm, ForgotPasswordForm
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from enter.send_email import Mail
from enter.models import UserInfo


class Login(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html", {"login": "请登录:", "login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("user")
            password = request.POST.get("password")
            all_login_info = json.loads(serializers.serialize("json", UserInfo.objects.filter(username=username)))
            if len(all_login_info) != 0:
                try:
                    username = all_login_info[0]['fields']['username']
                except IndexError:
                    return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})

                user = authenticate(username=username, password=password)
                if user:
                    url = request.GET.get("url")
                    ret = redirect(url if url else "/")
                    login(request, user=user)
                    request.session["user"] = username
                    request.session['is_login'] = "true"
                    request.session.set_expiry(None)
                    return ret
                else:
                    return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})
            else:
                return render(request, "login.html", {"login": "用户名或密码错误,请重新输入:", "login_form": login_form})
        else:
            return render(request, "login.html", {"login": "请登录:", "login_form": login_form})


class Logout(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect("/login/")


class SendEmail(APIView):
    def post(self, request):
        receiver = request.POST.get("receiver")
        method = request.POST.get("method")
        captcha = "".join([random.choice("0123456789") for _ in range(6)])
        if method == "register":
            try:
                Mail(receiver, captcha, method).send()
                if not models.RegisterCaptcha.objects.filter(email=receiver):
                    models.RegisterCaptcha(captcha=captcha, email=receiver, deadline=datetime.datetime.strptime(
                        (datetime.datetime.now() + datetime.timedelta(
                            minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")).save()
                else:
                    models.RegisterCaptcha.objects.filter(
                        email=receiver).update(captcha=captcha,
                                               deadline=datetime.datetime.strptime(
                                                   (datetime.datetime.now() + datetime.timedelta(
                                                       minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
            except:
                return JsonResponse({"error": 1})
            return JsonResponse({"error": 0})
        elif method == "forgot_password":
            try:
                Mail(receiver, captcha, method).send()
                if not models.ForgotPasswordCaptcha.objects.filter(email=receiver):
                    models.ForgotPasswordCaptcha(captcha=captcha, email=receiver,
                                                 deadline=datetime.datetime.strptime(
                                                     (datetime.datetime.now() + datetime.timedelta(
                                                         minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
                                                     "%Y-%m-%d %H:%M:%S")).save()
                else:
                    models.ForgotPasswordCaptcha.objects.filter(
                        email=receiver).update(captcha=captcha,
                                               deadline=datetime.datetime.strptime(
                                                   (datetime.datetime.now() + datetime.timedelta(
                                                       minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
            except:
                return JsonResponse({"error": 1})
            return JsonResponse({"error": 0})


class Register(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("username")
            nickname = request.POST.get("nickname")
            password = request.POST.get("first_password")
            captcha_email = request.POST.get("captcha_email")

            Adventure = "Adventure" if request.POST.get("Adventure") == "1" else ""
            Animation = "Animation" if request.POST.get("Animation") == "1" else ""
            Children = "Children" if request.POST.get("Children") == "1" else ""
            Comedy = "Comedy" if request.POST.get("Comedy") == "1" else ""
            Fantasy = "Fantasy" if request.POST.get("Fantasy") == "1" else ""
            Romance = "Romance" if request.POST.get("Romance") == "1" else ""
            Action = "Action" if request.POST.get("Action") == "1" else ""
            Crime = "Crime" if request.POST.get("Crime") == "1" else ""
            Thriller = "Thriller" if request.POST.get("Thriller") == "1" else ""
            Horror = "Horror" if request.POST.get("Horror") == "1" else ""
            FilmNoir = "FilmNoir" if request.POST.get("FilmNoir") == "1" else ""
            Drama = "Drama" if request.POST.get("Drama") == "1" else ""
            Mystery = "Mystery" if request.POST.get("Mystery") == "1" else ""
            SciFi = "SciFi" if request.POST.get("SciFi") == "1" else ""
            War = "War" if request.POST.get("War") == "1" else ""
            Western = "Western" if request.POST.get("Western") == "1" else ""
            Musical = "Musical" if request.POST.get("Musical") == "1" else ""
            IMAX = "IMAX" if request.POST.get("IMAX") == "1" else ""

            if not models.RegisterCaptcha.objects.filter(captcha=captcha_email):
                return render(request, "register.html",
                              {"register_error": "验证码输入有误！",
                               "register_form": register_form})
            else:
                if datetime.datetime.now() > datetime.datetime.strptime(
                        json.loads(
                            serializers.serialize(
                                "json",
                                models.RegisterCaptcha.objects.filter(
                                    captcha=captcha_email)))[0][
                            "fields"]["deadline"], "%Y-%m-%dT%H:%M:%S"):
                    return render(request, "register.html",
                                  {"register_error": "验证码已过期，请重新点击发送！",
                                   "register_form": register_form})
                else:
                    pass
            user_list = UserInfo.objects.filter(username=username)
            if user_list:
                return render(request, "register.html",
                              {"register_error": "该邮箱已注册！",
                               "register_form": register_form})
            elif username.strip() != '' and password.strip() != '':
                user = UserInfo.objects.create_user(
                    username=username, password=password, nickname=nickname)
                user.save()
                models.RegisterCaptcha.objects.filter(email=username).delete()
                now_user = model_to_dict(UserInfo.objects.get(username=username))
                now_user_id = now_user["id"]
                tags_list = list(
                    json.loads(serializers.serialize("json", Tags.objects.filter(Q(tagname__iexact=Adventure) | Q(
                        tagname__iexact=Animation) | Q(tagname__iexact=Children) | Q(tagname__iexact=Comedy) | Q(
                        tagname__iexact=Fantasy) | Q(tagname__iexact=Romance) | Q(tagname__iexact=Action) | Q(
                        tagname__iexact=Crime) | Q(tagname__iexact=Thriller) | Q(tagname__iexact=Horror) | Q(
                        tagname__iexact=FilmNoir) | Q(tagname__iexact=Drama) | Q(tagname__iexact=Mystery) | Q(
                        tagname__iexact=SciFi) | Q(tagname__iexact=War) | Q(tagname__iexact=Western) | Q(
                        tagname__iexact=Musical) | Q(tagname__iexact=IMAX)))))
                for item in tags_list:
                    UserSelectTags(userid=now_user_id, tagid=item["fields"]["tagid"]).save()
                return redirect("/login/")
        else:
            return render(request, "register.html", {"register_form": register_form})


class Modify(View):
    def get(self, request, method, username):
        if method == "nickname":
            register_form = RegisterForm()
            try:
                userdata = json.loads(
                    serializers.serialize("json",
                                          UserInfo.objects.filter(username=username)))[0]['fields']
            except IndexError as e:
                error = "该用户不存在！请勿通过修改URL的方式打开此页面。"
                back_button = "true"
                return render(request, "modify.html", locals())
            nickname = userdata['nickname']
            username = userdata['username']
            return render(request, "modify.html", locals())
        elif method == "password":
            register_form = RegisterForm()
            try:
                userdata = json.loads(
                    serializers.serialize("json",
                                          UserInfo.objects.filter(username=username)))[0]['fields']
            except IndexError as e:
                error = "该用户不存在！请勿通过修改URL的方式打开此页面。"
                back_button = "true"
                return render(request, "modify.html", locals())
            nickname = userdata['nickname']
            username = userdata['username']
            return render(request, "modify.html", locals())
        else:
            return render(request, "404.html")

    def post(self, request, method, username):
        register_form = RegisterForm(request.POST)
        if method == "nickname":
            nickname = request.POST.get("nickname")
            username = request.POST.get("username")
            user = UserInfo.objects.filter(username=username)
            try:
                user.update(nickname=nickname)
            except django.db.utils.DataError:  # 输入昵称超长
                return render(request, "modify.html", locals())
            return redirect("/")

        elif method == "password":
            username = request.POST.get("username")
            old_password = request.POST.get("old_password")
            user = authenticate(username=username, password=old_password)
            if not user:
                error = "旧密码输入有误，请重新输入！"
                return render(request, "modify.html", locals())
            first_password = request.POST.get("first_password")
            user.set_password(first_password)
            user.save()
            logout(request)
            return redirect("/login/")


# 忘记密码
class ForgotPassword(View):
    def get(self, request, username):
        forgot_password_form = ForgotPasswordForm()
        userdata = UserInfo.objects.filter(username=username)
        if not userdata:
            error = "该用户不存在！"
            back_button = "true"
            return render(request, "forgot_password.html", locals())
        return render(request, "forgot_password.html", locals())

    def post(self, request, username):
        forgot_password_form = ForgotPasswordForm(request.POST)
        username = request.POST.get("username")
        captcha_email = request.POST.get("captcha_email")

        if forgot_password_form.is_valid():
            if not models.ForgotPasswordCaptcha.objects.filter(captcha=captcha_email):
                return render(request, "forgot_password.html",
                              {"error": "验证码输入有误！", "username": username,
                               "forgot_password_form": forgot_password_form})
            else:
                if datetime.datetime.now() > datetime.datetime.strptime(json.loads(
                        serializers.serialize("json",
                                              models.ForgotPasswordCaptcha.objects.filter(captcha=captcha_email)))[0][
                                                                            "fields"]["deadline"], "%Y-%m-%dT%H:%M:%S"):
                    return render(request, "forgot_password.html",
                                  {"error": "验证码已过期，请重新点击发送！", "username": username,
                                   "forgot_password_form": forgot_password_form})
                else:
                    pass
            userdata = UserInfo.objects.get(username=username)
            first_password = request.POST.get("first_password")
            userdata.password = make_password(first_password)
            userdata.save()
            models.ForgotPasswordCaptcha.objects.filter(email=username).delete()
            return redirect("/login/")
        else:
            return render(request, "forgot_password.html",
                          {"forgot_password_form": forgot_password_form, "username": username})

# --------------------------------------------------------------------
# 注册发送邮箱验证码
# class SendEmailRegisterCodeView(APIView):
#     def get(self, request, *args, **kwargs):
#         return redirect('/register')
#
#     def post(self, request, *args, **kwargs):
#         ret = BaseResponseData()
#         try:
#             email = request.POST.get("email", None)
#
#             ret.data = {
#                 'code': "0", 'email': email, 'error_email': ''
#             }
#
#             user_obj = UserInfo.objects.filter(username=email, is_active=True).first()
#             if user_obj:
#                 ret.data['code'] = "111"
#                 ret.data['error_email'] = "用户已存在"
#                 return Response(ret.dict)
#             else:
#                 # 发送邮箱
#                 res_email = send_code_email(email)
#                 if res_email:
#                     # 注册用户信息，设置登陆状态为False
#                     create_last_user = UserInfo.objects.update_or_create(username=email, is_active=False)
#                     if not create_last_user:
#                         ret.data['code'] = "111"
#                         ret.data['error_email'] = "注册错误，请重试"
#                         return Response(ret.dict)
#                     return Response(ret.dict)
#                 else:
#                     ret.data['code'] = "111"
#                     ret.data['error_email'] = "验证码发送失败, 请稍后重试"
#                     return Response(ret.dict)
#         except Exception as e:
#             print("错误信息 : ", e)
#             ret.data['code'] = "111"
#             ret.data['error_email'] = "验证错误, 请稍后重试"
#         return Response(ret.dict)
