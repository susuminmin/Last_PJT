## 종합 프로젝트

# Open API를 활용한 날짜별 영화 정보 제공 사이트

> `DAY1` 2019-11-21 (목)

## 0. 프로젝트 목표 설정

- 영화진흥위원회 Open API, 네이버 영화 Open API 를 활용하여 영화 데이터를 수집한다. 
- VisualStudioCode 에서 Django 프레임워크를 이용한다.
- Bootstrap 을 이용하여 웹사이트 디자인을 구현한다. 
- 사용자의 조건 설정에 따라 영화 정보를 제공하는 사이트를 구현한다. 

---



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

---



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



* 코드를 실행하면 파일트리에 `movie.csv` 파일 생성

-------------

---------



> `Day2` 20191122 (금)

## 0.  목표

- csv파일 오류 수정
  
- csv파일 작성 시 필드네임을 수정해야 할 필요성을 느낌
    - 여러 주의 데이터를 연이어 받아올 때 영화정보 딕셔너리의 key 값을 영화이름으로 지정하면, 주가 바뀔 때 정보가 중복되는 문제점 발견
    - showRange 에 해당 주차 순위를 합친 새로운 변수 `기간순위` 를 포함한 필드를 새로 설정함. `기간순위`를 고유값으로 부여함으로써 문제 해결
  
- 영진위에서 만든 csv파일의 `영화제목`을 쿼리값으로 이용하여 네이버 영화API에서 썸네일URL 및 영화 줄거리 가져오기

  

  ## 1. 파일작성

  (1) movie.csv 파일 수정

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

  

  (2) 네이버API를 이용한 썸네일 및 줄거리 데이터 추가

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

  

  

----------

------------



> `Day03` 20191125 (월)

## 0. 목표

- 한 일

  ppt만들어서 페이지 구성해봄

  movies model, form 만들었다

  base.html을 만들건데, 로그인 여부에 따라 사이드바 내용을 바꾼다