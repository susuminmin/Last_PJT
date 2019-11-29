## 종합 프로젝트

# Open API를 활용한 날짜별 영화 정보 제공 사이트

> `DAY1` 2019-11-21 (목)

## 0. 프로젝트 목표 설정

- 영화진흥위원회 Open API, 네이버 영화 Open API 를 활용하여 영화 데이터를 수집한다. 
- VisualStudioCode 에서 Django 프레임워크를 이용한다.
- Bootstrap 을 이용하여 웹사이트 디자인을 구현한다. 
- 사용자의 조건 설정에 따라 영화 정보를 제공하는 사이트를 구현한다. 

### ERD

![1574986129079](C:\Users\student\AppData\Roaming\Typora\typora-user-images\1574986129079.png)



## 1. Django 프레임워크 초기 세팅

### 1-1. 가상환경

```shell
$ venv
$ python -m venv venv
```

* `Python: Select Intepreter` 에서 `'venv': venv` 설정



### 1-2. Django 프레임워크 설치

```shell
$ pip install django
```



### 1-3. Startproject, Startapp

```shell
$ django-admin startproject last-pjt .
```

```shell
$ python manage.py startapp accounts
$ python manage.py startapp movies
```



* `lastpjt` > `settings.py`에 앱 등록 

```python
# Application definition
INSTALLED_APPS = [
    # Local Apps
    'accounts',
    'movies',
	...
]
```



* `lastpjt` > `templates` 폴더에 `base.html` 작성

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
   <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <title>{% block title %}{% endblock title %}</title>
</head>
<body>
  {% block body %}
  {% endblock body %}

  <!-- Bootstrap JavaScript -->
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

* `base.html` 작성 후 반드시 `settings.py` 에 경로를 등록해 주어야 함.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'lastpjt', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```





## 2. `movie.csv` 파일 작성

* 별도로 생성한 `Movie_list.py` 에 영화진흥위원회 Open API 응답을 받아오는 코드 작성

```python
import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
key = config('API_KEY')
weekGb = '0'

with open('movie.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['기간', '영화코드', '영화제목', '순위']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(900):  
        # 2019년 ~ 2013년까지 약 900주의 데이터 불러오기
        targetDt = datetime(2019, 11, 17) - timedelta(weeks=i)
        targetDt = targetDt.strftime('%Y%m%d')
        API_URL = f'{BASE_URL}?key={key}&targetDt={targetDt}&weekGb=0'

        response = requests.get(API_URL)
        data = response.json()
        movie_data = {}

        showRange = data['boxOfficeResult']['showRange']

        for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
            movie_data[movie.get('movieCd')] = {
                '기간': showRange ,
                '영화코드': movie.get('movieCd'),
                '영화제목': movie.get('movieNm'),
                '순위': movie.get('rank'),
            }

        for item in movie_data.values():
            writer.writerow(item)

```

* 코드를 실행하면 파일트리에 `movie.csv` 파일 생성됨





---

> `Day2` 2019-11-22 (금)

## 0.  목표

- csv파일 오류 수정
  
- csv파일 작성 시 필드네임을 수정해야 할 필요성을 느낌
    - 여러 주의 데이터를 연이어 받아올 때 영화정보 딕셔너리의 key 값을 영화이름으로 지정하면, 주가 바뀔 때 정보가 중복되는 문제점 발견
    - showRange 에 해당 주차 순위를 합친 새로운 변수 `기간순위` 를 포함한 필드를 새로 설정함. `기간순위`를 고유값으로 부여함으로써 문제 해결
  
- 영진위에서 만든 csv파일의 `영화제목`을 쿼리값으로 이용하여 네이버 영화API에서 썸네일URL 및 영화 줄거리 가져오기

  

## 1. 파일작성

### 1-1. movie.csv 파일 수정

```python
import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
  
BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
key = config('API_KEY')
weekGb = '0'
  
# movie.csv라는 파일을 만들고, fieldnames대로 데이터를 채운다
with open('movie.csv', 'w', encoding='utf-8') as f:
	fieldnames = ['기간순위', '기간', '기간시작', '기간종료', '영화코드', '영화제목', '순위']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
  
    for i in range(5):
    	targetDt = datetime(2019, 11, 17) - timedelta(weeks=i)
        targetDt = targetDt.strftime('%Y%m%d')
        API_URL = f'{BASE_URL}?key={key}&targetDt={targetDt}&weekGb=0'
  
        response = requests.get(API_URL)
        data = response.json()
        movie_data = {}
  		
        # 우리가 원하는 데이터까지 접근
        showRange = data['boxOfficeResult']['showRange']
        start = showRange[:8]
        end = showRange[9:]
  		
        # 원하는 데이터 dict에서 for문을 돌면서 상세 데이터에 접근
        for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
        	movie_data[movie.get('movieCd')] = {
            	# str(기간)+str(순위) -> 다른데이터와 겹치지 않는 고유값을 만든다  
                '기간순위': showRange + movie.get('rank'),
                '기간': showRange,
               	'기간시작': start,
                '기간종료': end,
                '영화코드': movie.get('movieCd'),
                '영화제목': movie.get('movieNm'),
                '순위': movie.get('rank'),
            }
  
		for item in movie_data.values():
			writer.writerow(item)
            
```

  

  ### 1-2. 네이버API를 이용한 썸네일 및 줄거리 데이터 추가

  ```python
  import requests
  from pprint import pprint
  from decouple import config
  import csv
  import bs4
  from bs4 import BeautifulSoup
  
  BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
  clientId = config('CLIENT_ID')
  clientSecret = config('CLIENT_SECRET')
  HEADERS = {
      'X-Naver-Client-Id': clientId,
      'X-Naver-Client-Secret': clientSecret,
  }
  
  # 빈 qurey_dict 에 XXXXX (영화제목 값) 을 key로, {'영화코드': XXXXXXXX} 를 value 로 하는 자료 추가할 것 
  query_dict = {} 
  
  # 영진위에서 받아온 csv data의 '기간순위'값을 key로 data를 받아온다
  with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for row in reader:
          query_dict[row['기간순위']] = {
              '영화제목': row['영화제목'],
              '영화코드': row['영화코드'],
              '기간시작': row['기간시작'],
              '기간종료': row['기간종료'],
              '기간': row['기간'],
              '기간순위': row['기간순위'],
              }
  
  fieldnames = ('기간순위', '기간','기간시작', '기간종료', '썸네일_이미지의_URL', '영화제목', '영화코드', '하이퍼텍스트_링크', '줄거리')
  
  with open('movie_naver.csv', 'w', encoding='utf-8', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
      writer.writeheader()
  
      for week_rank, movie_dict in query_dict.items(): # key 값에 대한 for문
          movie_title = movie_dict['영화제목']
  
          API_URL = f'{BASE_URL}?query={movie_title}'
          response = requests.get(API_URL, headers=HEADERS).json()
  		
          # 데이터가 있을 때에만 받아오고, 데이터가 없다면 넘어간다
          try:
              link = response.get('items')[0].get('link')
              thumb_url = response.get('items')[0].get('image')
              movie_dict['하이퍼텍스트_링크'] = link
              movie_dict['썸네일_이미지의_URL'] = thumb_url
              # 네이버영화 상세페이지에 접근하여 줄거리 정보만 크롤링해온다.
              hyp_link = requests.get(link)
              html = hyp_link.text  
              soup = bs4.BeautifulSoup(html, 'html.parser')
              content = soup.select_one('div.story_area p.con_tx')
              movie_dict['줄거리'] = content.text
  
          except:
              pass
  
          writer.writerow(movie_dict)
  ```







---

> `Day03` 2019-11-25 (월)

## 1. Model 및 Form 정의

### 1-1.`movies` > `models.py`

```python
from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    poster_url = models.CharField(max_length=200)
    
    # M : N 관계
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
    month = models.CharField(max_length=3)
    day = models.CharField(max_length=3)
    # 사용자 입장에서 내가 검색한 모든 날짜 접근 => user.searched_dates.all()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='searched_dates', on_delete=models.CASCADE)

```



### 1-2. `movies` > `forms.py` 

```python
from django import forms
from .models import Review, SearchedDate


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['content', 'score', ]


class SearchedDateForm(forms.ModelForm):

    class Meta:
        model = SearchedDate
        fields = ['month', 'day']
```

```shell
$ python manage.py makemigrations
$ python manage.py migrate
```





## 2. 회원가입, 로그인, 로그아웃 기능 구현

### 2-1. `accounts` > `urls.py`

```python
from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('singup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
```



### 2-2. `accounts` > `views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def signup(request):  # 사용자에게 Form 제공해야 함
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        # 회원가입 로직
        form = UserCreationForm(request.POST)
        if form.is_valid():  # 잘 입력 되었는지 확인
            user = form.save()
            auth_login(request, user)  # 자동 로그인 기능
            # form.save()
            return redirect('movies:index')
    else:  # GET
        # 회원가입 페이지 보여주기
        # Form 을 context 에 담아서
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# 세션 데이터 만들기
# @login_required : GET 요청에서만 사용하면 됨 / 그러나 delete는 POST 라서 쓸 수 없음 // create, update는 GET 요청을 통해 그 페이지로 이동 ==> 그렇기 때문에 그 페이지로 이동하고자 할 때 login_required 사용되는 것
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        # 로그인 로직
        if form.is_valid():
            next_page = request.GET.get('next')  # url 붙은 str 꺼낼 때
            auth_login(request, form.get_user())  # 여기에만 request 들어간다
            # next 있으면 그 페이지로 보내고 아니면 index 페이지로 보내라 (중요!)
            # redirect 는 GET 요청만 지원 (주소창에 엔터치는 것과 동일한 일)
            return redirect(next_page or 'movies:index')
    else:
        # 로그인 = 세션 데이터 만드는 것 => UserCreationForm 사용 X AuthenticationForm 사용 O
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# 세션 정보 삭제
def logout(request):
    # POST, GET 구분 불필요
    auth_logout(request)
    return redirect('movies:index')

```



### 2-3. `accounts` > `templates` 

`login.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Template</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>

  <h1>로그인</h1>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">로그인</button>
  </form>


  <!-- Bootstrap JavaScript -->
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
    integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
    integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
    crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
    integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
    crossorigin="anonymous"></script>
</body>
</html>
```



`signup.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Template</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>

  <h1>회원가입</h1>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">회원가입</button>
  </form>


  <!-- Bootstrap JavaScript -->
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
    integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
    integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
    crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
    integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
    crossorigin="anonymous"></script>
</body>
</html>
```



### 3.  `Base.html` > Side Bar 만들기

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<style>
body {
    position: relative;
    overflow-x: hidden;
}
body,
html { height: 100%;}
.nav .open > a,
.nav .open > a:hover,
.nav .open > a:focus {background-color: transparent;}

/*-------------------------------*/
/*           Wrappers            */
/*-------------------------------*/

#wrapper {
    padding-left: 0;
    -webkit-transition: all 0.5s ease;
    -moz-transition: all 0.5s ease;
    -o-transition: all 0.5s ease;
    transition: all 0.5s ease;
}

#wrapper.toggled {
    padding-left: 220px;
}

#sidebar-wrapper {
   /* z-index는 태그들이 겹칠 때 누가 더 위로 올라가는지를 결정하는 속성, 기본값은 0 */
    z-index: 1000; /* z축 상의 위치를 나타내며, 정수값(음수, 양수). 높은 번호를 가진 레이어는 낮은 번호를 가진 레이어 위에 렌더링된다 */
    left: 220px;
    width: 0;
    height: 100%;
    margin-left: -220px;
    overflow-y: auto; /* 본문에 표시되는 내용에 따라 세로 스크롤이 생긴다. */
    overflow-x: hidden; /* 부모요소의 범위를 넘어가는 자식요소의 부분은 보이지 않도록 처리 */
    background: darkgray;
    -webkit-transition: all 0.5s ease; /* CSS 속성을 변경할 때 애니메이션 속도를 조절하는 방법을 제공 */
    -moz-transition: all 0.5s ease;
    -o-transition: all 0.5s ease;
    transition: all 0.5s ease;
}

#sidebar-wrapper::-webkit-scrollbar {
  display: none; /* 보이지 않음 */
}

#wrapper.toggled #sidebar-wrapper {
    width: 220px;
}

#page-content-wrapper {
    width: 100%;
    padding-top: 70px;
}

#wrapper.toggled #page-content-wrapper {
    position: absolute; /* 가장 가까운 곳에 위치한 조상 엘리먼트에 상대적으로 위치가 지정된다. */
    /* relative가 static인 상태를 기준으로 주어진 픽셀만큼 움직였다면, */
    /* absolute는 position: static 속성을 가지고 있지 않은 부모를 기준으로 움직인다. */
    /* 만약 부모 중에 포지션이 relative, absolute, fixed인 태그가 없다면 가장 위의 태그(body)가 기준이 된다. */
    margin-right: -220px;
}

/*-------------------------------*/
/*     Sidebar nav styles        */
/*-------------------------------*/

.sidebar-nav {
    position: absolute;
    top: 0;
    width: 220px;
    margin: 0;
    padding: 0;
    list-style: none;
}

.sidebar-nav li {
    position: relative;
    line-height: 20px;
    display: inline-block;
    width: 100%;
}

.sidebar-nav li:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
    height: 100%;
    width: 3px;
    background-color: #1c1c1c;
    -webkit-transition: width .2s ease-in;
      -moz-transition:  width .2s ease-in;
       -ms-transition:  width .2s ease-in;
            transition: width .2s ease-in;

}
.sidebar-nav li:first-child a {
    color: #fff;
    background-color: #1a1a1a;
}

.sidebar-nav li:before {
    background-color: #D8D8D8;  
}
.sidebar-nav li:hover:before,
.sidebar-nav li.open:hover:before {
    width: 100%;
    -webkit-transition: width .2s ease-in;
      -moz-transition:  width .2s ease-in;
       -ms-transition:  width .2s ease-in;
            transition: width .2s ease-in;

}

.sidebar-nav li a {
    display: block; /* 요소를 block 요소처럼 표시한다. 요소 앞뒤로 줄바꿈 된다. */
    color: #ddd;
    text-decoration: none; /* 선을 만들지 않는다. */
    padding: 10px 15px 10px 30px;    
}

.sidebar-nav li a:hover,
.sidebar-nav li a:active,
.sidebar-nav li a:focus,
.sidebar-nav li.open a:hover,
.sidebar-nav li.open a:active,
.sidebar-nav li.open a:focus{
    color: #fff;
    text-decoration: none;
    background-color: transparent;
}

.sidebar-nav > .sidebar-brand {
    height: 45px;
    font-size: 16px;
    line-height: 24px;
}
.sidebar-nav .dropdown-menu {
    position: relative;
    width: 100%;
    padding: 0;
    margin: 0;
    border-radius: 0;
    border: none;
    background-color: #222;
    box-shadow: none;
}

/*-------------------------------*/
/*       Link2me-Cross         */
/*-------------------------------*/

.link2me {
  position: fixed; /* fixed: 스크롤과 상관없이 항상 문서 최 좌측상단을 기준으로 좌표를 고정 */
  top: 20px;  
  z-index: 999; /* z-index는 태그들이 겹칠 때 누가 더 위로 올라가는지를 결정하는 속성, 기본값은 0 */
  display: block; /* 요소를 block 요소처럼 표시한다. 요소 앞뒤로 줄바꿈 된다. */
  width: 32px;
  height: 32px;
  margin-left: 15px;
  background: transparent;
  border: none;
}
.link2me:hover,
.link2me:focus,
.link2me:active {
  outline: none;
}
.link2me.is-closed:before {
  content: '';
  display: block;
  width: 100px;
  font-size: 14px;
  color: #fff;
  line-height: 32px;
  text-align: center;
  opacity: 0;
  -webkit-transform: translate3d(0,0,0);
  -webkit-transition: all .35s ease-in-out;
}
.link2me.is-closed:hover:before {
  opacity: 1;
  display: block;
  -webkit-transform: translate3d(-100px,0,0);
  -webkit-transition: all .35s ease-in-out;
}

.link2me.is-closed .hamb-top,
.link2me.is-closed .hamb-middle,
.link2me.is-closed .hamb-bottom,
.link2me.is-open .hamb-top,
.link2me.is-open .hamb-middle,
.link2me.is-open .hamb-bottom {
  position: absolute;
  left: 0;
  height: 4px;
  width: 100%;
}
.link2me.is-closed .hamb-top,
.link2me.is-closed .hamb-middle,
.link2me.is-closed .hamb-bottom {
  background-color: #1a1a1a;
}
.link2me.is-closed .hamb-top {
  top: 5px;
  -webkit-transition: all .35s ease-in-out;
}
.link2me.is-closed .hamb-middle {
  top: 50%;
  margin-top: -2px;
}
.link2me.is-closed .hamb-bottom {
  bottom: 5px;  
  -webkit-transition: all .35s ease-in-out;
}

.link2me.is-closed:hover .hamb-top {
  top: 0;
  -webkit-transition: all .35s ease-in-out;
}
.link2me.is-closed:hover .hamb-bottom {
  bottom: 0;
  -webkit-transition: all .35s ease-in-out;
}
.link2me.is-open .hamb-top,
.link2me.is-open .hamb-middle,
.link2me.is-open .hamb-bottom {
  background-color: #1a1a1a;
}
.link2me.is-open .hamb-top,
.link2me.is-open .hamb-bottom {
  top: 50%;
  margin-top: -2px;  
}
.link2me.is-open .hamb-top {
  -webkit-transform: rotate(45deg);
  -webkit-transition: -webkit-transform .2s cubic-bezier(.73,1,.28,.08);
}
.link2me.is-open .hamb-middle { display: none; }
.link2me.is-open .hamb-bottom {
  -webkit-transform: rotate(-45deg);
  -webkit-transition: -webkit-transform .2s cubic-bezier(.73,1,.28,.08);
}
.link2me.is-open:before {
  content: '';
  display: block;
  width: 100px;
  font-size: 14px;
  color: #fff;
  line-height: 32px;
  text-align: center;
  opacity: 0;
  -webkit-transform: translate3d(0,0,0);
  -webkit-transition: all .35s ease-in-out;
}
.link2me.is-open:hover:before {
  opacity: 1;
  display: block;
  -webkit-transform: translate3d(-100px,0,0);
  -webkit-transition: all .35s ease-in-out;
}

/*-------------------------------*/
/*            Overlay            */
/*-------------------------------*/

.overlay {
    position: fixed; /* fixed: 스크롤과 상관없이 항상 문서 최 좌측상단을 기준으로 좌표를 고정 */
    display: none;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(250,250,250,.8);
    z-index: 1;
}
.logout {
  margin: 7px 0 0 10px;
}

</style>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
<script>
$(document).ready(function () {
  var trigger = $('.link2me'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      link2me_cross();      
    });

    function link2me_cross() {

      if (isClosed == true) {          
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {   
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }
 
  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });  
});
</script>
</body>
    <div id="wrapper">
        <div class="overlay"></div>
    
        <!-- Sidebar 숨김으로 보였다 보이지 않았다 하는 부분 -->
        <nav class="navbar navbar-inverse navbar-fixed-top" id="sidebar-wrapper" role="navigation">
            <ul class="nav sidebar-nav">
            {% if user.is_authenticated %}
              <p class="logout">
              <a href="{% url 'accounts:logout' %}">로그아웃</a>
              </p>

              {% comment %} 사진, 이름을 보여주는 부분 {% endcomment %}
              <div class="text-center">
                <img src="{% static '프로필.jpg' %}" class="img-circle" width=100px height=100px><br>
                <span>{{ user.username }}</span><br>
              </div>
              {% comment %} 클릭한 영화, 날짜를 보여주는 부분 {% endcomment %}
              <h2>날짜</h2>
              {% for searched_date in searched_dates %}
                <p>{{ searched_date.date }}</p>
              {% endfor %}

              <h2>영화</h2>
              {% for click_movie in clicked_movies %}
                <p>{{ click_movie.title }}</p>
              {% endfor %}
                     
            {% else %}
            <p class="logout">
            <a href="{% url 'accounts:login' %}">로그인</a>
            <a href="{% url 'accounts:signup' %}">회원가입</a>
            </p>
            {% endif %}
          </ul>
        </nav>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <button type="button" class="link2me is-closed" data-toggle="offcanvas">
                <span class="hamb-top"></span>
                <span class="hamb-middle"></span>
                <span class="hamb-bottom"></span>
            </button>
            <div class="container">
                <div class="row">
                    <div class="col-lg-8 col-lg-offset-2">
                        <h1>{% block logo %}{% endblock logo %}</h1>
                        {% block body %}
                        {% endblock body %}
                    </div>
                </div>
            </div>
        </div>
        <!-- /#page-content-wrapper -->

    </div>
    <!-- /#wrapper -->
</body>
</html>

```





## 4. `views.py` 에서 index 및 movie_list 함수 정의 

* 앞서 정의한 모델을 본격적으로 활용할 movies 앱 내 페이지를 구현

### 4-1. `movies` > `urls.py` 에 movies 앱에서 사용할 url 정의

```python
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [

    path('movie_list/<int:date_pk>/', views.movie_list, name="movie_list"),
    path('', views.index, name="index"),
]
```



### 4-2. `movies` > `views.py`

* 우선 메인페이지(index.html) 에는 로그인한 유저에 한해 서비스를 제공한다. 
  * 사이드 바 부분에는 클릭한 영화, 검색한 날짜가 기록된다. 
  * 화면 중앙에는 월 / 일 입력 form 이 제공된다. 
* form 을 통해 월 / 일을 입력하면, 이에 해당하는 movie_list 페이지가 렌더링된다. 

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import Movie, Review, SearchedDate
from .forms import ReviewForm, SearchedDateForm


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
    date =  get_object_or_404(SearchedDate, pk=date_pk)
    context = {'date': date}
    return render(request, 'movies/movie_list.html', context)
```



### 4-3. `movies` > `templates` > `movies` 내 `html` 파일 생성

`index.html`

```html
{% extends 'base.html' %}

{% block logo %}그날의 박스오피스...
{% endblock logo %}


{% block body %}

  <form method="POST">
    {% csrf_token %}
    {{ dateform.as_p }}
    <button type="submit">로 돌아갈래....</button>
  </form>


{% endblock body %}
```



`movie_list` *(구체화 예정)*

```html
{% extends 'base.html' %}

{% block logo %}영화 검색 후 나올 페이지입니다.
{% endblock logo %}
{% block body %}
  성원아... {{ date.month }}월 {{ date.day }}일이야... 
{% endblock body %}
```

---



> `Day04` 2019-11-26 (화)

## 1. 네이버API를 통한 데이터 수집 완성

```python
import requests
from pprint import pprint
from decouple import config
import csv
import bs4
from bs4 import BeautifulSoup
import os
import django
from django.db import transaction


# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastpjt.settings")
django.setup()
# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from movies.models import Movie


BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
clientId = config('CLIENT_ID')
clientSecret = config('CLIENT_SECRET')
HEADERS = {
    'X-Naver-Client-Id': clientId,
    'X-Naver-Client-Secret': clientSecret,
}

query_dict = {} 
# 빈 qurey_dict 에 XXXXX (영화제목 값) 을 key로, {'영화코드': XXXXXXXX} 를 value 로 하는 자료 추가할 것 
with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        query_dict[row['기간순위']] = {
            '순위': row['순위'],
            # '기간': row['기간'],
            '기간시작': row['기간시작'],
            '기간종료': row['기간종료'],
            '영화코드': row['영화코드'],
            '영화명(국문)': row['영화명(국문)'],
            '기간순위': row['기간순위'],
            }

# 네이버에서 영화에 맞는 줄거리와 포스터url를 받아와서 dict에 합친 후,
# model.py의 MakeDB모델을 거쳐 우리 DB에 저장한다
fieldnames = ('순위', '기간시작', '기간종료', '썸네일_이미지의_URL', '영화명(국문)', '영화코드', '하이퍼텍스트_링크', '줄거리')
with open('movie_naver.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for week_rank, movie_dict in query_dict.items(): # key 값에 대한 for문
        movie_title = movie_dict['영화명(국문)']

        API_URL = f'{BASE_URL}?query={movie_title}'
        response = requests.get(API_URL, headers=HEADERS).json()
        
        try:
            link = response.get('items')[0].get('link')
            thumb_url = response.get('items')[0].get('image')
            movie_dict['하이퍼텍스트_링크'] = link
            movie_dict['썸네일_이미지의_URL'] = thumb_url
            # pprint(movie_dict)
            
            hyp_link = requests.get(link)
            # print(hyp_link.status_code)  /  200 -> 요청이 제대로 가짐
            # print('2', hyp_link)  /  200 -> 요청이 제대로 가짐
            html = hyp_link.text  # 응답받은 객체에서 html문서를 string으로 바꾸는 것
            soup = bs4.BeautifulSoup(html, 'html.parser')
            # print(soup)
            content = soup.select_one('div.story_area p.con_tx')
            movie_dict['줄거리'] = content.text

        except:
            pass

        writer.writerow(movie_dict)

        @transaction.atomic
        def make_model():
            movie = Movie()
            try:
                movie.start_date = movie_dict['기간시작']
            except:
                pass
            try:
                movie.end_date = movie_dict['기간종료']
            except:
                pass
            try:
                movie.rank = movie_dict['순위']
            except:
                pass
            try:
                movie.poster_url = movie_dict['썸네일_이미지의_URL']
            except:
                pass
            try:
                movie.title = movie_dict['영화명(국문)']
            except:
                pass
            try:
                movie.movie_code = movie_dict['영화코드']
            except:
                pass
            try:
                movie.naver_movie_url = movie_dict['하이퍼텍스트_링크']
            except:
                pass
            try:
                movie.description = movie_dict['줄거리']
            except:
                pass
            
            movie.save()

        if __name__ == "__main__":
            make_model()
            
```

* 기존에 영화진흥위원회 API 로 생성한 `movie.csv` 파일을 읽어온 후, 네이버 API 에서 추가적인 정보를 수집하여 `movie_naver.csv` 파일을 생성함과 동시에
* `movies` > `models.py` 에서 정의한 `Movie` 모델에 데이터를 업데이트한다. 



## 2. movie_list 페이지 완성

### 2-1 `movie_list.py`

```python
def movie_list(request, date_pk):
    user = request.user
    searched_dates = SearchedDate.objects.filter(user_id=user.id)
    # # date정보를 가져옴 (01/23)
    date = get_object_or_404(SearchedDate, pk=date_pk)
    # date19 = 20190000 + int(date.month + date.day)
    date18 = 20180000 + int(date.month + date.day)
    date17 = 20170000 + int(date.month + date.day)
    date16 = 20160000 + int(date.month + date.day)
    date15 = 20150000 + int(date.month + date.day)
    date14 = 20140000 + int(date.month + date.day)
    date13 = 20130000 + int(date.month + date.day)
    date12 = 20120000 + int(date.month + date.day)
    date11 = 20110000 + int(date.month + date.day)
    date10 = 20100000 + int(date.month + date.day)
    date09 = 20090000 + int(date.month + date.day)
    date08 = 20080000 + int(date.month + date.day)
    date07 = 20070000 + int(date.month + date.day)
    date06 = 20060000 + int(date.month + date.day)
    date05 = 20050000 + int(date.month + date.day)
    date04 = 20040000 + int(date.month + date.day)
    
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
    }
    return render(request, 'movies/movie_list.html', context)

```



### 2-2 `movie_list.html`

```html
{% extends 'base.html' %}

{% block logo %}
영화 검색 후 나올 페이지입니다.
<a href="{% url 'movies:index' %}">홈.으.로</a>
{% endblock logo %}


{% block body %}

  {{ date.month }}
  {{ date.day }} <br>

  {% for movie in movies18 %}
    {% if movie.rank <= 5 %}
    <img src="{{ movie.poster_url }}"><br>
    <a href="{% url 'movies:movie_review' movie.movie_code %}">{{ movie.rank }}. {{ movie.title }}<br></a>
    {% endif %}
  {% endfor %}

  {% for movie in movies17 %}
    {% if movie.rank <= 5 %}
    <img src="{{ movie.poster_url }}"><br>
    <a href="{% url 'movies:movie_review' movie.movie_code %}">{{ movie.rank }}. {{ movie.title }}<br></a>
    {% endif %}
  {% endfor %}

{% endblock body %}



{% block date %}

  {% for date in searched_dates %}
    <a href="{% url 'movies:movie_list' date.id %}">{{ date.month }}월 {{ date.day }}일<br></a> 
  {% endfor %}

{% endblock date %}

```

- 2018, 2017년의 사용자가 선택한 월/일 기간의 박스오피스 순위 영화 목록을 보여주는 페이지



## 3. movie_review 페이지 연동

### 3-1. `views.py`

```python
# movie_review

def movie_review(request, movie_code):
    user = request.user
    searched_dates = SearchedDate.objects.filter(user_id=user.id)
    movie = Movie.objects.filter(movie_code=movie_code).first()
    reviews = movie.reviews.all()
    review_form = ReviewForm()

    context = {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
        'searched_dates': searched_dates,
    }
    return render(request, 'movies/movie_review.html', context)
```

```python
# review_create

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
```



### 3-2. `movie_review.html` 

```html
{% extends 'base.html' %}
{% block logo %}Movie Review Page{% endblock logo %}
{% block body %}
  <h1>{{ movie.title }}</h1>
  <img src="{{ movie.poster_url }}" alt="image"><br>
  <br>
  {{ movie.description }}
  
  {% comment %} 리뷰 작성 {% endcomment %}
  <h3>Review</h3> 
  <ul>
    {% for review in reviews %}
      <li>{{ review.content }}
      {{ review.score }}점</li><br>
    {% endfor %}
  </ul>
  <form action="{% url 'movies:review_create' movie.movie_code %}"method="POST">
    {% csrf_token %}  
    {{ review_form.as_p }}
    <button type="submit">작성</button>
  </form>
  

{% endblock body %}

{% comment %} sidebar에 사용자가 검색한 날짜가 자동으로 업데이트됨 {% endcomment %}
{% block date %}
  {% for date in searched_dates %}
    <a href="{% url 'movies:movie_list' date.id %}">{{ date.month }}월 {{ date.day }}일<br></a> 
  {% endfor %}

{% endblock date %}
```

- 영화 코드를 기준으로, 가장 첫 번째 영화에 review를 작성할 수 있도록 구현

- 댓글과 점수를 남길 수 있다.

  

## 4. 검색한 날짜를 모두 띄우는 기능 구현

### 4-1 `index.html`

```python
# 사이드바에 기존에 검색한 날짜 목록을 띄운 후, 해당 날짜를 클릭하면 검색 결과로 이동하도록 설정

def index(request):
    # 로그인이 되어있을 경우에
    if request.user.is_authenticated:
        # 사이드바에서 제공할 데이터들
        user = request.user
        # 사용자가 클릭한 영화들 모두 가져오기  //  사용자가 검색한 날짜들 모두 가져오기
        clicked_movies = user.clicked_movies.all()
        # clicked_movies = Movie.objects.filter()
        # searched_dates = user.searched_dates.all()
        searched_dates = SearchedDate.objects.filter(user_id=user.id)
        # 월/일이 입력되었고, 내용을 담아서 movie_list 페이지로 보내줘야한다
        if request.method == 'POST':
            dateform = SearchedDateForm(request.POST)
            if dateform.is_valid():
                date = dateform.save(commit=False)
                date.user = request.user
                date.save()
                return redirect('movies:movie_list', date.pk)
        else:  # GET 요청
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
```





---------------------------------------

> `Day05` 2019-11-27 (수)

## 1. 리뷰 페이지에 접속한 영화를 sidebar에 표시하는 기능 구현 

* `index.html` 및 `movie_list.html` , `movie_review.html` 각각에 side-bar 표시할 내용 입력

```html
...
{% block date %}

{% for date in searched_dates %}
  <a href="{% url 'movies:movie_list' date.id %}" class="sidebar_date">{{ date.month }}월 {{ date.day }}일<br></a> 
{% endfor %}

{% endblock date %} 


{% comment %} sidebar에 영화 넣는 부분 {% endcomment %}
{% block sidemovie %}

{% for movie in clicked_movies %}
  
  <img src="{{ movie.poster_url }}" class="sidebar_card"><br>
  <div class="card-body">
    <h4 class="card-title"><a href="{% url 'movies:movie_review' movie.movie_code %}">{{ movie.title }}</a><br></h4>
  </div>
  
{% endfor %}

{% endblock sidemovie %}

```



## 2. `movie_list.html` 에서 영화 카드 배치 수정

* `movie_list.html` 의 `{% block body %}` 와 `{% endblock body %}` 사이에 2018년부터 2004년까지 영화 정보 표시

```html
{% extends 'base.html' %}
{% block logo %}
<div class="title">
  {{ date.month }}월 {{ date.day }}일의 영화 순위
</div>
{% endblock logo %}

{% block body %}
<div class="container">
  <p><h3>2018년 Top4</h3></p>
  {% for movie in movies18 %}
  {% if movie.rank <= 4 %}
  <div class="b-blcok col-xl-3 col-lg-3 col-md-3 col-3">
    <div class="card bg-white" style="width: 16rem;">
      <img src="{{ movie.poster_url }}" class="card-img-top">
      <div class="card-body">
        <h4 class="card-title"><a href="{% url 'movies:movie_review' movie.movie_code %}">{{ movie.title }}<br></a><br>
        </h4>
      </div>
    </div>
  </div>
  {% endif %}
  {% endfor %}
</div>

...

{% endblock body %}

```



## 3. movies 앱 내 배경 이미지 삽입

### 3-1. `base.html` css style 추가

```html
    body {
      background-image: url(https://i.redd.it/vcu684cde8y01.jpg);
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      background-attachment: fixed;
      position: relative;
      overflow-x: hidden;
    }
```



---

> `DAY1` 2019-11-28 (목)

## 1. 로그인 및 회원가입 페이지 css style 적용

### 1-1. `accounts` > `forms.py`

```python
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        label='Username',
        max_length=254,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label='Username',
        max_length=254,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', ]
```

* 커스터마이징 하기 위해 form 세부정보를 지정
* `accounts` > `views.py` 에서도 `CustomAuthenticationForm` 및 `CustomUserCreationForm` 사용



### 1-2. `login.html` 

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Template</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <style>
    body {
      background-image: url(https://i.redd.it/vcu684cde8y01.jpg);
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      background-attachment: fixed;
      position: relative;
      overflow-x: hidden;
    }
  </style>
</head>
<body>
  <div class="home">
    <a href="{% url 'movies:index' %}"><span class="glyphicon glyphicon-home fa-lg"></span></a>
  </div>

  <h2 style="color: #c6bfca">로그인</h2>
  <form method="POST">
    {% csrf_token %}
    <p style="color: #c6bfca">
    Username {{ empty }}{{ form.username }}<br>{{ empty }}
    Password {{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ form.password }}
    </p>
    <button type="submit">로그인</button>
  </form>

...
    
</body>
</html>
```



### 1-3. `signup.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Template</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <style>
    body {
      background-image: url(https://i.redd.it/vcu684cde8y01.jpg);
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      background-attachment: fixed;
      position: relative;
      overflow-x: hidden;
    }
  </style>
</head>
<body>

  <h2 style="color: #c6bfca">회원가입</h2>
  <form method="POST">
    {% csrf_token %}
    <p style="color: #c6bfca">
    Username {{ empty }}{{ form.username }}<br>{{ empty }}
    Password {{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ form.password1 }}
    Repeat Password {{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ empty }}{{ form.password2 }}

    </p>
    <button type="submit">회원가입</button>
  </form>

    ...
    
</body>
</html>
```

---







## 느낀점

- 조성원

  ```
  저희조는 장르나 배우 이름을 이용한 영화추천 서비스대신 새로운 영화 추천 방식을 사용해보고 싶었습니다.
  그래서 '특정 요일을 입력받으면 15년동안 그 날의 영화 순위'를 보여주는 영화추천 사이트를 주제로 정했습니다.
  가장 힘들었던 점은 DB를 만드는 일이었습니다. csv파일을 바로 django 내 데이터로 만들 수 있도록 설정하는데도 많은 시간이 걸렸습니다. 또한, 프로젝트를 진행함에 따라 DB모델이 계속 바뀌게 되었고 그에 따라 DB도 계속해서 다시 받아야 했습니다. 이 경험으로 처음부터 데이터와 모델들의 관계를 제대로 설정하는 것이 중요하다는걸 알았습니다.
  
  또, 팀원 간 의사소통의 어려움과 중요성을 알게되었습니다. 제가 만들고자 하는 모델을 이해시키는 것과, 팀원이 얘기하려는 것을 한번에 이해하는 것이 생각보다 힘들었습니다. 처음에는 서로 자신의 말만 반복하는 것 같았지만 나중에는 쉬운 설명을 위해 그림을 그리거나 ppt를 사용하여 의사소통의 효율을 높였습니다.
  
  저 혼자 프로젝트를 해야했다면 일주일이 지나도 기본적인 회원가입, 로그인 기능밖에 구현하지 못했을 것이라고 생각합니다. 제가 모르는 점을 팀원이 잘 받쳐주었기 때문에 길지 않은 시간 내에 프로젝트를 완성할 수 있었던 것 같습니다.
  ```



- 김수민

  ```
  한 학기동안 웹 개발을 배우면서 부족한 점이 많다는 생각이 들었는데, 페어 프로그래밍으로 최종 프로젝트를 하면서 부족한 점을 많이 보완할 수 있었습니다. 특히, 웹의 큰 구조, 틀에 대한 이해가 부족해서 어느 부분이 잘못되었는지 이해하는데 가장 큰 어려움을 느꼈습니다.
  
하지만 짝과 함께 개발을 할 때에는 서로에게 부족한 점을 이해하고 넘어가야 했기 때문에 부족한 부분을 반드시 이해하고 넘어가야 했습니다. 이 때문에 기존에 공부하면서 부족하다고 생각했던 점이 빠르게 보완할 수 있었습니다. 
  
  이와 비슷한 방식으로 다른 프레임워크를 활용한다면 한 학기동안 아쉬웠던 점에 대해 빠르게 보완할 수 있으리라 생각합니다. 이번 프로젝트를 통해 자신감과 성취감을 얻을 수 있었습니다.
  ```
  
  