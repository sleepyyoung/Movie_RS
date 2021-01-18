import random

from django.forms import model_to_dict
from django.views import View
from django.utils.decorators import method_decorator
from api import models
from django.core import serializers
import json
from django.http import HttpResponse
from enter.models import UserInfo
from home.views import loginORnot
from Arithmetic.arithmetic import Recommend


class RecommendForYou(View):
    @method_decorator(loginORnot)
    def get(self, request):
        # 13张大图
        username = request.session.get("user")
        userid = model_to_dict(UserInfo.objects.get(username=username))["id"]
        # 换一换   基于用户的协同过滤
        r = Recommend()
        movieid_list = random.sample([_[0] for _ in r.Recommenduser(str(userid), r.UserCF(), 2000)], 50)

        imdbid_list = []
        for movieid in movieid_list:
            imdbid_list.append(json.loads(
                serializers.serialize("json",
                                      models.Links.objects.filter(movieid=movieid)))[0]["fields"]["imdbid"])
        big_all = []
        for imdbid in imdbid_list:
            big_all.append(
                json.loads(serializers.serialize("json", models.IMDb_Detail.objects.filter(imdbid="00" + str(imdbid)))))
        all = []
        for item in big_all:
            if len(item) != 0:
                all.append(item[0]["fields"])
        return HttpResponse(json.dumps(all[:12]))
