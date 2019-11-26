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
        # 사이드바에서 제공할 데이터들
        user = request.user
        # 사용자가 클릭한 영화들 모두 가져오기  //  사용자가 검색한 날짜들 모두 가져오기
        clicked_movies = user.clicked_movies.all()
        searched_dates = user.searched_dates.all()
        
        # 월/일이 입력되었고, 내용을 담아서 movie_list 페이지로 보내줘야한다
        if request.method == 'POST':
            dateform = SearchedDateForm(request.POST)
            if dateform.is_valid():
                date = dateform.save(commit=False)
                date.user = request.user
                date.save()
                return redirect('movies:movie_list', date.pk)
        else: # GET 요청
            dateform = SearchedDateForm()

        context = {
        'clicked_movies': clicked_movies,
        'searched_dates': searched_dates,
        'dateform': dateform,
        }
        return render(request, 'movies/index.html', context)


    # 로그인 X 유저일 경우 아예 아무 것도 못 함
    else:
        dateform = SearchedDateForm()
        return render(request, 'movies/index.html', {'dateform': dateform})
    
    
def movie_list(request, date_pk):
    # date정보를 가져옴 (01/23)
    date = get_object_or_404(SearchedDate, pk=date_pk)
    target = date.month + date.day
    

    for year in range(2004, 2019):
        with open('movies/movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
            items = csv.DictReader(f)
            new_target = int(str(year) + target)

            for item in items:
                start = int(item['기간시작'])
                end = int(item['기간종료'])

                if start <= new_target <= end:
                    rank = item['기간순위'][-1]
                    title = item['영화제목']
                    poster_url = item['썸네일_이미지의_URL']
                    discription = item['줄거리']
                    naver_movie_url = item['하이퍼텍스트_링크']
                    # print(rank, title, poster_url, discription, naver_movie_url)


    context = {
        'rank': rank,
        'title': title,
        # 'result': 20180000 + 100 * int(date.month) + int(date.day)
    }
    
    return render(request, 'movies/movie_list.html', context)