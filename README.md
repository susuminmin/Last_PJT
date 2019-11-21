## 종합 프로젝트

# Open API를 활용한 날짜별 영화 정보 제공 사이트

> `DAY1` 2019-11-21 (목)

### 0. 프로젝트 목표 설정

- 영화진흥위원회 Open API, 네이버 영화 Open API 를 활용하여 영화 데이터를 수집한다. 
- VisualStudioCode 에서 Django 프레임워크를 이용한다.
- Bootstrap 을 이용하여 웹사이트 디자인을 구현한다. 
- 사용자의 조건 설정에 따라 영화 정보를 제공하는 사이트를 구현한다. 

---



### 1. Django 프레임워크 초기 세팅

#### 1-1. 가상환경

```shell
$ venv
$ python -m venv venv
```

* `Python: Select Intepreter` 에서 `'venv': venv` 설정



#### 1-2. Django 프레임워크 설치

```shell
$ pip install django
```



#### 1-3. Startproject, Startapp

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



### 2. `movie.csv` 파일 작성

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

    for i in range(3):
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