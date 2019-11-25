from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    poster_url = models.CharField(max_length=200)
    clicked_users = models.ManyToManyField( # movie.clicked_users.all()  =>  해당 영화를 클릭한 모든 유저를 불러오는 방법
        settings.AUTH_USER_MODEL,
        related_name='clicked_movies'  # user.clicked_movies.all()  =>  해당 유저가 클릭만 모든 영화를 불러오는 방법
    )


class Review(models.Model):
    content = models.CharField(max_length=50)
    score = models.IntegerField()
    # 사용자 입장에서 내가 작성한 댓글들에 접근할 때 => user.reviews.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    # 영화 입장에서 나한테 달린 댓글들에 접근할 때 => movie.reviews.all()
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk', )


class SearchedDate(models.Model):
    date = models.DateField()
    # 사용자 입장에서 내가 검색한 모든 날짜 접근 => user.searched_dates.all()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='searched_dates',on_delete=models.CASCADE) 



