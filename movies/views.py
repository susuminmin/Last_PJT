from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Movie, Review, SearchedDate
from .forms import ReviewForm, SearchedDateForm
from decouple import config
import csv


def index(request):
    # 로그인이 되어있을 경우에
    if request.user.is_authenticated:
        user = request.user
        searched_dates = SearchedDate.objects.filter(user_id=user.id)
        clicked_movies = user.clicked_movies.all()

        if request.method == 'POST':
            month = request.POST.get('month')
            day = request.POST.get('day')
            last_dates = SearchedDate.objects.filter(user_id=user.id)

            # 기존 검색해 본 날짜를 돌면서, 중복된 검색 날짜가 있으면 바로 그 날짜를 검색하게 한다. 
            for date in last_dates:
                if date.month == month and date.day == day:
                    return redirect('movies:movie_list', date.pk)    

            date = SearchedDate()
            date.month = month
            date.day = day
            date.user = request.user
            date.save()
            
            return redirect('movies:movie_list', date.pk)
        else:  # GET 요청
            dateform = SearchedDateForm()
        context = {
            'clicked_movies': clicked_movies,
            'searched_dates': searched_dates,
            'dateform': dateform,
            'user': user,
        }
        return render(request, 'movies/index.html', context)
    # 로그인 X 유저일 경우 아예 아무 것도 못 함
    else:
        dateform = SearchedDateForm()
        return render(request, 'movies/index.html', {'dateform': dateform})


def movie_list(request, date_pk):
    user = request.user
    clicked_movies = user.clicked_movies.all()
    searched_dates = SearchedDate.objects.filter(user_id=user.id)
    # # date정보를 가져옴 (01/23)
    date = get_object_or_404(SearchedDate, pk=date_pk)
    
    date18 = 20180000 + int(date.month) * 100 + int(date.day)
    date17 = 20170000 + int(date.month) * 100 + int(date.day)
    date16 = 20160000 + int(date.month) * 100 + int(date.day)
    date15 = 20150000 + int(date.month) * 100 + int(date.day)
    date14 = 20140000 + int(date.month) * 100 + int(date.day)
    date13 = 20130000 + int(date.month) * 100 + int(date.day)
    date12 = 20120000 + int(date.month) * 100 + int(date.day)
    date11 = 20110000 + int(date.month) * 100 + int(date.day)
    date10 = 20100000 + int(date.month) * 100 + int(date.day)
    date09 = 20090000 + int(date.month) * 100 + int(date.day)
    date08 = 20080000 + int(date.month) * 100 + int(date.day)
    date07 = 20070000 + int(date.month) * 100 + int(date.day)
    date06 = 20060000 + int(date.month) * 100 + int(date.day)
    date05 = 20050000 + int(date.month) * 100 + int(date.day)
    date04 = 20040000 + int(date.month) * 100 + int(date.day)
    
    movies18 = Movie.objects.filter(
        start_date__lte=date18,
        end_date__gte=date18,
    )
    movies17 = Movie.objects.filter(
        start_date__lte=date17,
        end_date__gte=date17,
    )
    movies16 = Movie.objects.filter(
        start_date__lte=date16,
        end_date__gte=date16,
    )
    movies15 = Movie.objects.filter(
        start_date__lte=date15,
        end_date__gte=date15,
    )
    movies14 = Movie.objects.filter(
        start_date__lte=date14,
        end_date__gte=date14,
    )
    movies13 = Movie.objects.filter(
        start_date__lte=date13,
        end_date__gte=date13,
    )
    movies12 = Movie.objects.filter(
        start_date__lte=date12,
        end_date__gte=date12,
    )
    movies11 = Movie.objects.filter(
        start_date__lte=date11,
        end_date__gte=date11,
    )
    movies10 = Movie.objects.filter(
        start_date__lte=date10,
        end_date__gte=date10,
    )
    movies09 = Movie.objects.filter(
        start_date__lte=date09,
        end_date__gte=date09,
    )
    movies08 = Movie.objects.filter(
        start_date__lte=date08,
        end_date__gte=date08,
    )
    movies07 = Movie.objects.filter(
        start_date__lte=date07,
        end_date__gte=date07,
    )
    movies06 = Movie.objects.filter(
        start_date__lte=date06,
        end_date__gte=date06,
    )
    movies05 = Movie.objects.filter(
        start_date__lte=date05,
        end_date__gte=date05,
    )
    movies04 = Movie.objects.filter(
        start_date__lte=date04,
        end_date__gte=date04,
    )

    context = {
        'date': date,
        'movies18': movies18,
        'movies17': movies17,
        'movies16': movies16,
        'movies15': movies15,
        'movies14': movies14,
        'movies13': movies13,
        'movies12': movies12,
        'movies11': movies11,
        'movies10': movies10,
        'movies09': movies09,
        'movies08': movies08,
        'movies07': movies07,
        'movies06': movies06,
        'movies05': movies05,
        'movies04': movies04,
        'searched_dates': searched_dates,
        'clicked_movies': clicked_movies,
    }
    return render(request, 'movies/movie_list.html', context)


def movie_review(request, movie_code):
    user = request.user
    
    # 내가 클릭한 영화 (현재)
    movie = Movie.objects.filter(movie_code=movie_code).first()

    # 내(user)가 기존에 클릭해 본 영화들 
    clicked_movies = user.clicked_movies.all()

    flag = False
    for last_movie in clicked_movies:
        if last_movie.title == movie.title:
            flag = True

    if flag == False: # 지금 클릭한 영화가 처음 클릭한 영화인 경우
       user.clicked_movies.add(movie)

    searched_dates = SearchedDate.objects.filter(user_id=user.id)    
    clicked_movies = user.clicked_movies.all()
    
    reviews = movie.reviews.all()
    review_form = ReviewForm()

    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
        'searched_dates': searched_dates,
        'clicked_movies': clicked_movies,
    }
    return render(request, 'movies/movie_review.html', context)


def review_create(request, movie_code):
    movie = Movie.objects.filter(movie_code=movie_code).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie.id
            review.user_id = request.user.id
            review.save()
        
        return redirect('movies:movie_review', movie_code)
