from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('movie_review/<int:movie_code>',
         views.movie_review, name="movie_review"),
    path('movie_list/<int:date_pk>/', views.movie_list, name="movie_list"),
    path('', views.index, name="index"),
]
