# 그날의 영화
> 날짜별 영화 정보 제공 서비스

## General info

![](img/screenshot.png)

https://github.com/sungwoncho94/Movie_recommend_PJT

## Technologies
* Django - 2.2.7
* Bootstrap 4
* Python - 3.7.4
  

## Setup

- 다음과 같은 방법으로 필요 모듈을 다운받고 앱을 실행할 수 있습니다.

> 가상환경 설치 후, Python: Select Interpreter에서 'venv' 설정

```bash
$ python -m venv venv
```

> requirements.txt에 있는 모듈 설치

```bash
$ pip install -r requirements.txt 
```

> Django 앱 실행하기

```bash
$ python manage.py runserver
```



## Features
* 회원가입, 로그인

  * 로그인 상태에서만 서비스를 이용할 수 있습니다.
  * 로그인 시 사이드바에 검색 내역이 나타납니다.
  * 클릭하면 기존에 조회한 영화 혹은 날짜 페이지로 이동합니다.
    

* 4월 1일을 검색하면 2018년 ~ 2004년 박스오피스 TOP 1~4 영화 목록이 조회됩니다.

  * 영화 목록 페이지에는 영화 포스터와 영화명이 제공됩니다.
  * 영화명을 클릭하면 영화 상세보기 페이지로 이동합니다.

  ![](img/date_search_to_detail_page.gif)
  


* 영화 상세보기 페이지에서는 영화제목, 출연 배우, 네이버 영화 링크, 영화 포스터, 줄거리를 제공합니다.
  
  ![](img/review_and_sidebar.gif)

## Status
알파 버전 개발 중
배포 예정

## Author
조성원, 김수민