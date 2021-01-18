import datetime
import re
import time
from functools import wraps

from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.views import View
from api import models
from django.core import serializers
import json
from enter.models import UserInfo
from Arithmetic.arithmetic import Recommend


def loginORnot(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")
        request.session.clear_expired()
        if is_login != "true":
            return redirect(f"/login/?url={request.path_info}")
        ret = func(request, *args, **kwargs)
        return ret

    return inner


class RecommendForYou(View):
    @method_decorator(loginORnot)
    def get(self, request):
        is_login = request.session.get("is_login", "")
        username = request.session.get("user", "")
        nickname = model_to_dict(UserInfo.objects.get(username=username))["nickname"]
        all = []
        user_id = model_to_dict(UserInfo.objects.get(username=username))["id"]
        tags = {user_id: [item["fields"]["tagid"] for item in json.loads(
            serializers.serialize("json", models.UserSelectTags.objects.filter(userid=user_id)))]}
        r = Recommend()
        # 冷启动  利用新用户选择的感兴趣标签随机推荐
        movieid_list = r.RecommendTagNuser(user_id, r.Tag(), tags, 50)
        imdbid_list = []
        for movieid in movieid_list:
            imdbid_list.append(model_to_dict(models.Links.objects.get(movieid=movieid))["imdbid"])
        all = []
        for item in imdbid_list:
            obj = json.loads(serializers.serialize("json", models.IMDb_Detail.objects.filter(imdbid="00" + item)))
            if len(obj) != 0:
                all.append(dict({
                    "title": obj[0]["fields"]["title"],
                    "summary": obj[0]["fields"]["summary"],
                    "imdbid": obj[0]["fields"]["imdbid"],
                }))
        all3 = all[:3]
        all2 = all[3:5]
        all_small4 = all[5:9]
        all_big4 = all[9:13]
        return render(request, "recommand.html", locals())


class Douban_250(View):
    def get(self, request):
        is_login = request.session.get("is_login", "false")
        if is_login == "true":
            username = request.session.get("user", "")
            if username != "":
                nickname = model_to_dict(UserInfo.objects.get(username=username)).get("nickname", "")
            else:
                nickname = ""
        else:
            username = ""
        all = []
        for item in json.loads((json.dumps(
                json.loads(serializers.serialize("json", models.DoubanRank.objects.filter().order_by("srank"))),
                ensure_ascii=False))):
            all.append(dict({
                "srank": item["fields"]["srank"],
                "href": item["fields"]["href"],
                "director": item["fields"]["director"],
                "screenwriter": item["fields"]["screenwriter"],
                "actor": item["fields"]["actor"],
                "type": item["fields"]["type"],
                "country": item["fields"]["country"],
                "language": item["fields"]["language"],
                "release_time": item["fields"]["release_time"],
                "duration": item["fields"]["duration"],
                "nickname": item["fields"]["nickname"],
                "imdb_link": item["fields"]["imdb_link"],
                "img_href": item["fields"]["img_href"],
                "title": item["fields"]["title"],
                "score": item["fields"]["score"],
                "evaluator": item["fields"]["evaluator"],
            }))
        paginator = Paginator(all, 10)
        result_num = len(all)
        tail_page = paginator.num_pages
        tail_page_ellipsis = tail_page - 4

        try:
            current_num = request.GET.get('page', "1")
            if current_num.isnumeric() and int(current_num) >= 1:
                current_num = int(current_num)
            else:
                current_num = 1

            all = paginator.page(current_num)
            if tail_page > 11:
                if current_num - 5 < 1:
                    page_range = range(1, 11)
                elif current_num + 5 > tail_page:
                    page_range = range(tail_page - 9, tail_page + 1)
                else:
                    page_range = range(current_num - 5, current_num + 5)
            else:
                page_range = paginator.page_range
            return render(request, 'douban_250.html', locals())
        except EmptyPage:
            error_page = request.GET.get('page')
            if error_page.isnumeric():
                if int(error_page) < 1:
                    return redirect(redirect(request.path + "?page=1"))
                elif int(error_page) > int(tail_page):
                    return redirect(request.path + "?page=" + str(tail_page))
            else:
                return redirect(request.path + "?page=1")


class Select(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TYPE = [
            '全部',
            '冒险(Adventure)',  # Adventure
            '动画(Animation)',  # Animation
            '儿童(Children)',  # Children
            '喜剧(Comedy)',  # Comedy
            '幻想(Fantasy)',  # Fantasy
            '爱情(Romance)',  # Romance
            '动作(Action)',  # Action
            '犯罪(Crime)',  # Crime
            '惊悚(Thriller)',  # Thriller
            '恐怖(Horror)',  # Horror
            '暗黑(Film-Noir)',  # Film-Noir
            '戏剧(Drama)',  # Drama
            '神秘(Mystery)',  # Mystery
            '科幻(Sci-Fi)',  # Sci-Fi
            '战争(War)',  # War
            '西部(Western)',  # Western
            '音乐(Musical)',  # Musical
        ]
        # self.YEAR = ["全部"] + [str(_) for _ in range(1971, 2017)]
        self.YEAR = ["全部"] + [str(_) for _ in range(2018, 1999, -1)] + [
            "90年代", "80年代", "70年代", "60年代", "50年代", "更早"]
        self.sort_method = ["评分倒序", "评分正序", "时间倒序", "时间正序"]

    def get(self, request):
        is_login = request.session.get("is_login")
        if is_login:
            username = request.session.get("user")
            if username:
                nickname = model_to_dict(UserInfo.objects.get(username=username))["nickname"]
            else:
                pass
        else:
            pass
        TYPE, YEAR, SORT_METHOD = self.TYPE, self.YEAR, self.sort_method
        p = request.GET.get("p", "0-0-0")
        url = request.path + "?p=" + p
        type_, year, sort_method = p.split("-")[0], p.split("-")[1], p.split("-")[2]
        type_ = int(type_) if type_.isnumeric else 0
        year = int(year) if year.isnumeric else 0
        sort_method = int(sort_method) if sort_method.isnumeric else 0
        order_by = "-score"
        if sort_method == 1:
            order_by = "score"
        elif sort_method == 2:
            order_by = "-year"
        elif sort_method == 3:
            order_by = "year"

        orm_type = re.findall(r"\((.*?)\)", TYPE[type_], re.S)[0] if TYPE[type_] != "全部" else 0
        orm_year = YEAR[year]
        if orm_year == "全部":
            orm_year = [1900, 2020]
        elif orm_year == "90年代":
            orm_year = [1990, 1999]
        elif orm_year == "80年代":
            orm_year = [1980, 1989]
        elif orm_year == "70年代":
            orm_year = [1970, 1979]
        elif orm_year == "60年代":
            orm_year = [1960, 1969]
        elif orm_year == "50年代":
            orm_year = [1950, 1959]
        elif orm_year == "更早":
            orm_year = [1900, 1949]
        else:
            orm_year = [int(orm_year), int(orm_year) + 1]
        all = []
        objs = models.IMDb_Detail.objects.filter(
            ~Q(year="None"),
            the_type__contains=orm_type if orm_type != 0 else "",
            year__range=orm_year).order_by(order_by)
        for item in json.loads((json.dumps(
                json.loads(serializers.serialize("json", objs)),
                ensure_ascii=False))):
            all.append(dict({
                "imdbid": item["fields"]["imdbid"],
                "imdb_link": item["fields"]["imdb_link"],
                "picture_link": item["fields"]["picture_link"],
                "title": item["fields"]["title"],
                "year": item["fields"]["year"],
                "score": item["fields"]["score"],
                "rating_count": item["fields"]["rating_count"],
                "summary": item["fields"]["summary"],
                "director": item["fields"]["director"],
                "writers": item["fields"]["writers"],
                "stars": item["fields"]["stars"],
            }))
        paginator = Paginator(all, 48)
        result_num = len(all)
        tail_page = paginator.num_pages
        tail_page_ellipsis = tail_page - 4

        try:
            current_num = request.GET.get('page', "1")
            if current_num.isnumeric() and int(current_num) >= 1:
                current_num = int(current_num)
            else:
                current_num = 1

            all = paginator.page(current_num)
            if tail_page > 11:
                if current_num - 5 < 1:
                    page_range = range(1, 11)
                elif current_num + 5 > tail_page:
                    page_range = range(tail_page - 9, tail_page + 1)
                else:
                    page_range = range(current_num - 5, current_num + 5)
            else:
                page_range = paginator.page_range
            return render(request, 'select.html', locals())
        except EmptyPage:
            error_page = request.GET.get('page')
            error_page = int(error_page) if type(eval(error_page)) == int else "1"
            if error_page > tail_page:
                return redirect(request.path + "?page=" + str(tail_page) + "&" + p)
            else:
                return redirect(request.path + "?page=1" + "&" + p)


class GetDetail(View):
    def get(self, request, imdbid):
        is_login = request.session.get("is_login", "")
        username = request.session.get("user", "")
        if is_login != "" and username != "":
            nickname = model_to_dict(UserInfo.objects.get(username=username))["nickname"]
            userid = model_to_dict(UserInfo.objects.get(username=username))["id"]
            movieid = model_to_dict(models.Links.objects.get(imdbid=imdbid[2:]))["movieid"]
            history = list(
                json.loads(serializers.serialize("json", models.Rating.objects.filter(userid=userid, movieid=movieid))))
            score = ""
            if len(history) != 0:
                score = history[0]["fields"]["rating"]

            time_ = datetime.datetime(
                int(time.strftime('%Y', time.localtime(time.time()))),
                int(time.strftime('%m', time.localtime(time.time()))),
                int(time.strftime('%d', time.localtime(time.time()))),
                int(time.strftime('%H', time.localtime(time.time()))),
                int(time.strftime('%M', time.localtime(time.time()))),
                int(time.strftime('%S', time.localtime(time.time()))),
            )
            if len(list(json.loads(
                    serializers.serialize("json",
                                          models.BrowseRecords.objects.filter(username=username,
                                                                              imdbid=imdbid))))) == 0:
                models.BrowseRecords(username=username, imdbid=imdbid, time=time_).save()
            else:
                models.BrowseRecords.objects.filter(username=username, imdbid=imdbid).update(time=time_)
        try:
            detail = json.loads(
                (json.dumps(
                    json.loads(serializers.serialize('json', models.IMDb_Detail.objects.filter(imdbid=imdbid))),
                    ensure_ascii=False)))[0]
        except IndexError:
            error_flag = "1"
            return render(request, "404.html", locals())
        all = {
            "imdbid": detail["fields"]["imdbid"],
            "imdb_link": detail["fields"]["imdb_link"],
            "picture_link": detail["fields"]["picture_link"],
            "title": detail["fields"]["title"],
            "year": detail["fields"]["year"],
            "score": detail["fields"]["score"],
            "rating_count": detail["fields"]["rating_count"],
            "length": detail["fields"]["length"],
            "the_type": detail["fields"]["the_type"],
            "premiere": detail["fields"]["premiere"],
            "summary": detail["fields"]["summary"].replace("Add a Plot", "").replace("»", ""),
            "director": detail["fields"]["director"].replace("Directors:", "").replace("Director:", ""),
            "writers": detail["fields"]["writers"],
            "stars": detail["fields"]["stars"],
            "story_line": detail["fields"]["story_line"],
            "did_you_know": detail["fields"]["did_you_know"],
        }
        return render(request, "detail.html", locals())

    @method_decorator(loginORnot)
    def post(self, request, imdbid):
        username = request.session.get("user")
        userid = model_to_dict(UserInfo.objects.get(username=username))["id"]
        score = request.POST.get("score")
        movieid = model_to_dict(models.Links.objects.get(imdbid=imdbid[2:]))["movieid"]
        history = list(
            json.loads(serializers.serialize("json", models.Rating.objects.filter(userid=userid, movieid=movieid))))
        if len(history) == 0:
            # models.Rating(userid=userid, rating=score, movieid=movieid).save()
            models.Rating.objects.create(userid=userid, movieid=movieid, rating=score)
        else:
            models.Rating.objects.filter(userid=userid, movieid=movieid).update(rating=score)
        return redirect(request.path)


class Search(View):
    def get(self, request):
        is_login = request.session.get("is_login")
        if is_login:
            username = request.session.get("user")
            if username:
                nickname = model_to_dict(UserInfo.objects.get(username=username))["nickname"]
            else:
                pass
        else:
            pass
        kw = request.GET.get("kw", "")
        all = []
        for item in json.loads((json.dumps(
                json.loads(serializers.serialize("json", models.IMDb_Detail.objects.filter(title__contains=kw).order_by(
                    "-score"))),
                ensure_ascii=False))):
            all.append(dict({
                "imdbid": item["fields"]["imdbid"],
                "imdb_link": item["fields"]["imdb_link"],
                "picture_link": item["fields"]["picture_link"],
                "title": item["fields"]["title"],
                "year": item["fields"]["year"],
                "score": item["fields"]["score"],
                "rating_count": item["fields"]["rating_count"],
                "summary": item["fields"]["summary"],
                "director": item["fields"]["director"],
                "writers": item["fields"]["writers"],
                "stars": item["fields"]["stars"],
            }))

        paginator = Paginator(all, 48)
        result_num = len(all)
        tail_page = paginator.num_pages
        tail_page_ellipsis = tail_page - 4

        try:
            current_num = request.GET.get('page', "1")
            if current_num.isnumeric() and int(current_num) >= 1:
                current_num = int(current_num)
            else:
                current_num = 1

            all = paginator.page(current_num)
            if tail_page > 11:
                if current_num - 5 < 1:
                    page_range = range(1, 11)
                elif current_num + 5 > tail_page:
                    page_range = range(tail_page - 9, tail_page + 1)
                else:
                    page_range = range(current_num - 5, current_num + 5)
            else:
                page_range = paginator.page_range
            return render(request, 'search.html', locals())
        except EmptyPage:
            error_page = request.GET.get('page')
            error_page = int(error_page) if type(eval(error_page)) == int else "1"
            if error_page > tail_page:
                return redirect(request.path + "&page=" + str(tail_page))
            else:
                return redirect(request.path + "&page=1")


class BrowseRecords(View):
    @method_decorator(loginORnot)
    def get(self, request):
        is_login = request.session.get("is_login")
        username = request.session.get("user")
        nickname = model_to_dict(UserInfo.objects.get(username=username))["nickname"]
        results = json.loads(
            serializers.serialize("json",
                                  models.BrowseRecords.objects.filter(username=username).order_by("-time")))

        all = []
        for item in results:
            username = item["fields"]["username"]
            imdbid = item["fields"]["imdbid"]
            time_ = str(item["fields"]["time"]).replace("T", " ")
            movie = model_to_dict(models.IMDb_Detail.objects.get(imdbid=imdbid))
            title = movie.get("title", "")
            year = movie.get("year", "")
            score = movie.get("score", "")
            rating_count = movie.get("rating_count", "")
            length = movie.get("length", "")
            the_type = movie.get("the_type", "")
            premiere = movie.get("premiere", "")
            director = movie.get("director", "")
            writers = movie.get("writers", "")
            stars = movie.get("stars", "")

            all.append(dict({
                "username": username,
                "imdbid": imdbid,
                "time": time_,
                "title": title,
                "year": year,
                "score": score,
                "rating_count": rating_count,
                "length": length,
                "the_type": the_type,
                "premiere": premiere,
                "director": director,
                "writers": writers,
                "stars": stars,
            }))

        paginator = Paginator(all, 10)
        result_num = len(all)
        tail_page = paginator.num_pages
        tail_page_ellipsis = tail_page - 4

        try:
            current_num = request.GET.get('page', "1")
            if current_num.isnumeric() and int(current_num) >= 1:
                current_num = int(current_num)
            else:
                current_num = 1
            all = paginator.page(current_num)
            if tail_page > 11:
                if current_num - 5 < 1:
                    page_range = range(1, 11)
                elif current_num + 5 > tail_page:
                    page_range = range(tail_page - 9, tail_page + 1)
                else:
                    page_range = range(current_num - 5, current_num + 5)
            else:
                page_range = paginator.page_range
            return render(request, 'browse_records.html', locals())
        except EmptyPage:
            error_page = request.GET.get('page')
            if error_page.isnumeric():
                if int(error_page) < 1:
                    return redirect(redirect(request.path + "?page=1"))
                elif int(error_page) > int(tail_page):
                    return redirect(request.path + "?page=" + str(tail_page))
            else:
                return redirect(request.path + "?page=1")
        return render(request, "browse_records.html", locals())
