from django.db import models
from django.conf import settings


# MakeDB모델을 거쳐서 movie.csv -> 네이버API -> (Django MakeDB모델) -> DB
class Movie(models.Model):
    # 필요한 정보 : rank, 국문 title, 영문 title, description, poster_url, naver_movie_url, -> csv에서부터 db를 만들기 위해 필요한 필드
    # range_rank = models.CharField(max_length=30)
    # showRange = models.CharField(max_length=30)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    rank = models.IntegerField()
    poster_url = models.CharField(max_length=200)
    title = models.CharField(max_length=20)
    movie_code = models.CharField(max_length=30)
    naver_movie_url = models.CharField(max_length=200)
    description = models.TextField()
    clicked_users = models.ManyToManyField(  # movie.clicked_users.all()  =>  해당 영화를 클릭한 모든 유저를 불러오는 방법
        settings.AUTH_USER_MODEL,
        # user.clicked_movies.all()  =>  해당 유저가 클릭만 모든 영화를 불러오는 방법
        related_name='clicked_movies'
    )


class Review(models.Model):
    content = models.CharField(max_length=50)
    score = models.IntegerField()
    # 사용자 입장에서 내가 작성한 댓글들에 접근할 때 => user.reviews.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='reviews', on_delete=models.CASCADE)
    # 영화 입장에서 나한테 달린 댓글들에 접근할 때 => movie.reviews.all()
    movie = models.ForeignKey(
        Movie, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk', )


class SearchedDate(models.Model):
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)
    # 사용자 입장에서 내가 검색한 모든 날짜 접근 => user.searched_dates.all()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='searched_dates', on_delete=models.CASCADE)
