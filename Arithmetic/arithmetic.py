import pandas as pd
import math
import pandas
import random


class Recommend:
    def __init__(self):
        self.MOVIES_CSV = "Arithmetic/movies.csv"
        self.RATINGS_CSV = "Arithmetic/ratings.csv"
        self.RATINGS_DATA_CSV = "Arithmetic/ratings_data.csv"
        self.GENOMETR_DATA_CSV = "Arithmetic/genomeTR_data.csv"
        self.result_list = []
        self.movies = pd.read_csv(self.MOVIES_CSV)  # 9000
        self.ratings = pd.read_csv(self.RATINGS_CSV)  # 十万
        # 筛选平均评分大于2.0分的电影
        self.num = self.ratings.groupby(['movieId'])['rating'].mean()
        self.movies_num = self.num[self.num >= 2.0]
        # 根据平均评分进行排序
        self.rat = list(self.movies_num)
        self.mID = list(self.movies_num.index)
        self.mID = [str(i) for i in self.mID]
        self.mID1 = zip(self.mID, self.rat)
        self.nvDict = dict((self.mID, movie) for self.mID, movie in self.mID1)
        self.movie_list = sorted(self.nvDict.items(), key=lambda x: x[1], reverse=True)
        self.movie_sort = [x for x, _ in self.movie_list]
        # 筛选平均评分大于4分的电影
        self.ratings_data = self.ratings[self.ratings.movieId.isin(self.movies_num.index)]
        self.movies_data = self.movies[self.movies.movieId.isin(self.movies_num.index)]
        self.ratings = pd.read_csv(self.RATINGS_DATA_CSV)
        self.file1 = open(self.RATINGS_DATA_CSV, 'r', encoding='UTF-8')
        self.data = {}  # 存放每位用户评论的电影和评分
        for line in self.file1.readlines()[1:100000]:
            # 注意这里不是readline()
            line = line.strip().split(',')
            # 如果字典中没有某位用户，则使用用户ID来创建这位用户
            if not line[0] in self.data.keys():
                self.data[line[0]] = {line[1]: line[2]}
            # 否则直接添加以该用户ID为key字典中
            else:
                self.data[line[0]][line[1]] = line[2]
        # #转化为矩阵形式
        # df = pandas.DataFrame(data).T.fillna(0)
        # 建立电影-标签矩阵
        self.file2 = open(self.GENOMETR_DATA_CSV, 'r', encoding='UTF-8')
        self.dataT = {}
        for line in self.file2.readlines()[1:100000]:
            # 注意这里不是readline()
            line = line.strip().split(',')
            if not line[0] in self.dataT.keys():
                self.dataT[line[0]] = {line[1]: line[2]}
            else:
                self.dataT[line[0]][line[1]] = line[2]

    # 1.基于用户的协同过滤
    def UserCF(self):
        # 计算item->user的倒排索引
        item_users = {}
        for user in self.data:
            for item in self.data[user]:
                if item not in item_users:
                    item_users[item] = []
                item_users[item].append(user)

        # 计算用户相似度矩阵
        C = {}
        N = {}  # 用户曾经有过正反馈的物品集合
        for item in item_users:
            users = item_users[item]
            for i in range(len(users)):
                u = users[i]
                if u not in N:
                    N[u] = 0
                N[u] += 1
                if u not in C:
                    C[u] = {}
                for j in range(len(users)):
                    if j == i: continue
                    v = users[j]
                    if v not in C[u]:
                        C[u][v] = 0
                    C[u][v] += 1

        # 相似度矩阵
        W = {}
        for u in C:
            if u in C:
                W[u] = {}
            for v in C[u]:
                if v in C[u]:
                    W[u][v] = 0
                W[u][v] = C[u][v] / math.sqrt(N[u] * N[v])
        return W

    # 计算评分实现推荐
    def Recommenduser(self, user, W, K):
        rank = {}
        seen_items = self.data[user]
        user_sorted = sorted(W[user].items(), key=lambda item: item[1], reverse=True)[0:K]
        downfactor = 0
        for i in range(len(user_sorted)):
            downfactor += user_sorted[i][1]
        for v, W in sorted(W[user].items(), key=lambda item: item[1], reverse=True)[0:K]:
            for movie, rating in self.data[v].items():
                # 判断要推荐的电影该用户曾经没有过反馈
                if movie in seen_items:
                    continue
                rank.setdefault(movie, 0)  # 返回该键对应的value
                rank[movie] += float(W) * float(rating)
        for key, value in rank.items():
            rank[key] = value / downfactor
        result = sorted(rank.items(), key=lambda item: item[1], reverse=True)[0:K]
        return result

    # 2.基于电影的协同过滤
    def MovieCF(self):
        # 计算user->item的倒排索引
        item_users = {}
        for user in self.data:
            for item in self.data[user]:
                if item not in item_users:
                    item_users[item] = []
                item_users[item].append(user)

        users_item = dict()
        for movie in item_users:
            for item in item_users[movie]:
                if item not in users_item:
                    users_item[item] = []
                users_item[item].append(movie)

        # 计算电影相似度矩阵
        C = {}
        N = {}
        for item in users_item:
            movie = users_item[item]
            for i in range(len(movie)):
                u = movie[i]
                if u not in N:
                    N[u] = 0
                N[u] += 1
                if u not in C:
                    C[u] = {}
                for j in range(len(movie)):
                    if j == i: continue
                    v = movie[j]
                    if v not in C[u]:
                        C[u][v] = 0
                    C[u][v] += 1

        # 相似度矩阵
        W = {}
        for i, related_items in C.items():
            W.setdefault(i, {})
            for j, cij in related_items.items():
                W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return W

    # 计算评分实现推荐
    def Recommendmovie(self, user, W, K):
        rank = {}
        Sum = {}
        ru = self.data[user]
        result = []
        for i, rating in ru.items():
            movie_sort = sorted(W[i].items(), key=lambda item: item[1], reverse=True)[0:K]
            for j, wj in movie_sort:
                if j in ru.keys():
                    continue
                Sum.setdefault(j, [])
                rank.setdefault(j, 0)
                if j not in ru.keys():
                    Sum[j].append(wj)
                rank[j] += float(rating) * float(wj)

            result = dict(sorted(rank.items(), key=lambda item: item[1], reverse=True)[0:K])
            for key in result:
                result[key] = result[key] / sum(Sum[key])
            result = sorted(result.items(), key=lambda item: item[1], reverse=True)[0:K]
        return result

    # 3.随机推荐
    def Random(self):
        items = {}
        for user in self.data:
            for item in self.data[user]:
                items[item] = 1
        return items

    # 实现推荐
    def Recommendrandom(self, user, items, N):
        # 随机推荐N个未见过的
        user_items = set(self.data[user])
        rec_items = {k: items[k] for k in items if k not in user_items}
        rec_items = list(rec_items.keys())
        random.shuffle(rec_items)
        # 推荐N部电影
        # print(rec_items[:N])
        return rec_items[:N]

    # 4.热门推荐
    def Recommendpopular(self, user, N):
        rec_items = []
        for i in self.movie_sort:
            if i not in self.data[user]:
                rec_items.append(i)
        # print(rec_items[:N])
        return rec_items[:N]

    # 用户的冷启动问题
    # 1.利用新用户选择的感兴趣标签随机推荐
    def Tag(self):
        # 计算tags->movie的倒排索引
        tags_movie = {}
        for movie in self.dataT:
            for tag in self.dataT[movie]:
                if tag not in tags_movie:
                    tags_movie[tag] = []
                tags_movie[tag].append(movie)
        return tags_movie

    # 实现推荐
    def RecommendTagNuser(self, user, train, dict, N):
        rec_items = []
        for key in dict.get(user):
            if key in train:
                for movie in train[key]:
                    rec_items.append(movie)
        random.shuffle(rec_items)
        # print(rec_items[:N])
        return rec_items[:N]

    # 2.利用新用户浏览足迹推荐
    def TagHistory(self):
        # 计算item->tags的倒排索引
        tags_movie = {}
        for movie in self.dataT:
            for tag in self.dataT[movie]:
                if tag not in tags_movie:
                    tags_movie[tag] = []
                tags_movie[tag].append(movie)

        movie_tags = dict()
        for tag in tags_movie:
            for movie in tags_movie[tag]:
                if movie not in movie_tags:
                    movie_tags[movie] = []
                movie_tags[movie].append(tag)
        return movie_tags

    # 实现推荐
    def RecommendHistoryNuser(self, user, train1, dict, N):
        rec_items = []
        Tag = []
        for movie in dict[user]:
            if movie in self.dataT:
                for tag in self.dataT[movie]:
                    Tag.append(tag)
                    for i in Tag:
                        if i in train1:
                            for j in train1[i]:
                                if j not in rec_items:
                                    if j not in dict[user]:
                                        rec_items.append(j)
        random.shuffle(rec_items)
        # print(rec_items[:N])
        return rec_items[:N]


# r = Recommend()
# user = '3'
# N = 10
# a = {3: ['19', '29', '64', '323', '686', '863']}

# 1.基于用户的协同过滤
# user_CF = r.UserCF()
# user_CF_result = [i for i, j in r.Recommenduser(user, user_CF, N)]
# print(user_CF_result)
# #
# # 2.基于电影的协同过滤
# movie_CF = r.MovieCF()
# movie_CF_result = [i for i, j in r.Recommendmovie(user, movie_CF, N)]
# print(movie_CF_result)
#
# # 3.随机推荐
# random_data = r.Random()
# recommend_random = r.Recommendrandom(user, random_data, N)
# print(recommend_random)
#
# # 4.热门推荐dict[user]
# recommend_popular = r.Recommendpopular(user, N)
# print(recommend_popular)
#
# # 用户的冷启动问题
# # 1.利用新用户选择的感兴趣标签随机推荐
# tag_dataT = r.Tag()
# recommend_tag_user = r.RecommendTagNuser(user, tag_dataT, a, N)
# print(recommend_tag_user)
#
# # 2.利用新用户浏览足迹推荐
# tag_history = r.TagHistory()
# recommend_tag_history = r.RecommendHistoryNuser(user, tag_dataT, a, N)
# print(recommend_tag_history)


"""
result_list = []

movies = pd.read_csv('./movies.csv')  # 9000
ratings = pd.read_csv('./ratings.csv')  # 十万
# genomeTR = pd.read_csv('./genome-scores.csv')
# links = pd.read_csv('./links.csv')

# 筛选平均评分大于2.0分的电影
num = ratings.groupby(['movieId'])['rating'].mean()
movies_num = num[num >= 2.0]
# 根据平均评分进行排序
rat = list(movies_num)
mID = list(movies_num.index)
mID = [str(i) for i in mID]
mID1 = zip(mID, rat)
nvDict = dict((mID, movie) for mID, movie in mID1)
movie_list = sorted(nvDict.items(), key=lambda x: x[1], reverse=True)
movie_sort = [x for x, _ in movie_list]
# print(movie_sort)


# 筛选平均评分大于4分的电影
ratings_data = ratings[ratings.movieId.isin(movies_num.index)]
# 生成新的ratings_data.csv
# ratings_data.to_csv(path_or_buf='ratings_data.csv', index=False)
# print(ratings_data)
movies_data = movies[movies.movieId.isin(movies_num.index)]
# 生成新的movies_data.csv
# movies_data.to_csv(path_or_buf='movies_data.csv', index=False)
# print(movies_data)
# 只保留电影与标签相关性大于90%的标签
# genomeTR_data = genomeTR[genomeTR.movieId.isin(movies_num.index)]
# genomeTR_data = genomeTR_data.drop(index=genomeTR_data.loc[(genomeTR_data['relevance'] < 0.90)].index)
# 生成新的电影-标签csv表
# genomeTR_data.to_csv(path_or_buf='genomeTR_data.csv', index=False)
# print(genomeTR_data)
# links_data = links[links.movieId.isin(movies_num.index)]
# print(links_data)
# links_data.to_csv(path_or_buf='links_data.csv', index=False)


ratings = pd.read_csv('./ratings_data.csv')
# 建立用户-电影评分矩阵
file = open("ratings_data.csv", 'r', encoding='UTF-8')
# 读取ratings_data.csv中每行中除了名字的数据
data = {}  # 存放每位用户评论的电影和评分
for line in file.readlines()[1:100000]:
    # 注意这里不是readline()
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[1]: line[2]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[1]] = line[2]

# #转化为矩阵形式
df = pandas.DataFrame(data).T.fillna(0)
# print(data)
# print(df)


# 建立电影-标签矩阵
file = open("./genomeTR_data.csv", 'r', encoding='UTF-8')
dataT = {}
for line in file.readlines()[1:100000]:
    # 注意这里不是readline()
    line = line.strip().split(',')
    if not line[0] in dataT.keys():
        dataT[line[0]] = {line[1]: line[2]}
    else:
        dataT[line[0]][line[1]] = line[2]


# 1.基于用户的协同过滤
def UserCF(train):
    # 计算item->user的倒排索引
    item_users = {}
    for user in train:
        for item in train[user]:
            if item not in item_users:
                item_users[item] = []
            item_users[item].append(user)

    # 计算用户相似度矩阵
    C = {}
    N = {}  # 用户曾经有过正反馈的物品集合
    for item in item_users:
        users = item_users[item]
        for i in range(len(users)):
            u = users[i]
            if u not in N:
                N[u] = 0
            N[u] += 1
            if u not in C:
                C[u] = {}
            for j in range(len(users)):
                if j == i: continue
                v = users[j]
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1

    # 相似度矩阵
    W = {}
    for u in C:
        if u in C:
            W[u] = {}
        for v in C[u]:
            if v in C[u]:
                W[u][v] = 0
            W[u][v] = C[u][v] / math.sqrt(N[u] * N[v])
    return W


# 计算评分实现推荐
def Recommenduser(user, train, W, K):
    rank = {}
    seen_items = train[user]
    user_sorted = sorted(W[user].items(), key=lambda item: item[1], reverse=True)[0:K]
    downfactor = 0
    for i in range(len(user_sorted)):
        downfactor += user_sorted[i][1]
    for v, W in sorted(W[user].items(), key=lambda item: item[1], reverse=True)[0:K]:
        for movie, rating in train[v].items():
            # 判断要推荐的电影该用户曾经没有过反馈
            if movie in seen_items:
                continue
            rank.setdefault(movie, 0)  # 返回该键对应的value
            rank[movie] += float(W) * float(rating)
    for key, value in rank.items():
        rank[key] = value / downfactor
    result = sorted(rank.items(), key=lambda item: item[1], reverse=True)[0:K]
    return (result)


# 2.基于电影的协同过滤
def MovieCF(train):
    # 计算user->item的倒排索引
    item_users = {}
    for user in train:
        for item in train[user]:
            if item not in item_users:
                item_users[item] = []
            item_users[item].append(user)

    users_item = dict()
    for movie in item_users:
        for item in item_users[movie]:
            if item not in users_item:
                users_item[item] = []
            users_item[item].append(movie)

    # 计算电影相似度矩阵
    C = {}
    N = {}
    for item in users_item:
        movie = users_item[item]
        for i in range(len(movie)):
            u = movie[i]
            if u not in N:
                N[u] = 0
            N[u] += 1
            if u not in C:
                C[u] = {}
            for j in range(len(movie)):
                if j == i: continue
                v = movie[j]
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1

    # 相似度矩阵
    W = {}
    for i, related_items in C.items():
        W.setdefault(i, {})
        for j, cij in related_items.items():
            W[i][j] = cij / (math.sqrt(N[i] * N[j]))
    return W


# 计算评分实现推荐
def Recommendmovie(user_id, train, W, K):
    rank = {}
    Sum = {}
    ru = train[user_id]
    for i, rating in ru.items():
        movie_sort = sorted(W[i].items(), key=lambda item: item[1], reverse=True)[0:K]
        for j, wj in movie_sort:
            if j in ru.keys():
                continue
            Sum.setdefault(j, [])
            rank.setdefault(j, 0)
            if j not in ru.keys():
                Sum[j].append(wj)
            rank[j] += float(rating) * float(wj)

        result = dict(sorted(rank.items(), key=lambda item: item[1], reverse=True)[0:K])
        for key in result:
            result[key] = result[key] / sum(Sum[key])
        result = sorted(result.items(), key=lambda item: item[1], reverse=True)[0:K]
    return result


# 3.随机推荐
def Random(train):
    items = {}
    for user in train:
        for item in train[user]:
            items[item] = 1
    return items


# 实现推荐
def Recommendrandom(user, train, items, N):
    # 随机推荐N个未见过的
    user_items = set(train[user])
    rec_items = {k: items[k] for k in items if k not in user_items}
    rec_items = list(rec_items.keys())
    random.shuffle(rec_items)
    # 推荐N部电影
    print(rec_items[:N])


# 4.热门推荐
def Recommendpopular(user, train, N):
    rec_items = []
    for i in movie_sort:
        if i not in train[user]:
            rec_items.append(i)
    print(rec_items[:N])


# 用户的冷启动问题
# 1.利用新用户选择的感兴趣标签随机推荐
def Tag(train):
    # 计算tags->movie的倒排索引
    tags_movie = {}
    for movie in train:
        for tag in train[movie]:
            if tag not in tags_movie:
                tags_movie[tag] = []
            tags_movie[tag].append(movie)
    return tags_movie


# 实现推荐
def RecommendTagNuser(user, train, dict, N):
    rec_items = []
    for key in dict[user]:
        if key in train:
            for movie in train[key]:
                rec_items.append(movie)
    random.shuffle(rec_items)
    print(rec_items[:N])


# 2.利用新用户浏览足迹推荐
def TagHistory(train):
    # 计算item->tags的倒排索引
    tags_movie = {}
    for movie in train:
        for tag in train[movie]:
            if tag not in tags_movie:
                tags_movie[tag] = []
            tags_movie[tag].append(movie)

    movie_tags = dict()
    for tag in tags_movie:
        for movie in tags_movie[tag]:
            if movie not in movie_tags:
                movie_tags[movie] = []
            movie_tags[movie].append(tag)
    return movie_tags


# 实现推荐
def RecommendHistoryNuser(user, train, train1, dict, N):
    rec_items = []
    Tag = []
    for movie in dict[user]:
        if movie in train:
            for tag in train[movie]:
                Tag.append(tag)
                for i in Tag:
                    if i in train1:
                        for j in train1[i]:
                            if j not in rec_items:
                                if j not in dict[user]:
                                    rec_items.append(j)
    random.shuffle(rec_items)
    print(rec_items[:N])
"""

# user_CF = UserCF(data)
# user_CF_result = [i for i, j in Recommenduser('1', data, user_CF, 10)]
# print(user_CF_result)

# movie_CF = MovieCF(data)
# movie_CF_result = [i for i, j in Recommendmovie('1', data, movie_CF, 10)]
# print(movie_CF_result)

# random_data = Random(data)
# Recommendrandom('9', data, random_data, 10)
#
# Recommendpopular('600', data, 10)

# a = dict()
# a = {'1': ['63', '863', '78'], '3': ['3', '7', '45', '4', '9']}

# tag_dataT = Tag(dataT)
# RecommendTagNuser("1", tag_dataT, a, 13)
#
# tag_history = TagHistory(dataT)
# RecommendHistoryNuser('3', tag_history, tag_dataT, a, 10)
