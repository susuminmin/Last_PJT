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

query_dict = {} 
# 빈 qurey_dict 에 XXXXX (영화제목 값) 을 key로, {'영화코드': XXXXXXXX} 를 value 로 하는 자료 추가할 것 
with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        query_dict[row['기간순위']] = {
            '순위': row['순위'],
            '기간': row['기간'],
            '영화코드': row['영화코드'],
            '영화명(국문)': row['영화명(국문)'],
            '기간순위': row['기간순위'],
            '기간시작': row['기간시작'],
            '기간종료': row['기간종료'],
            }

# pprint(query_dict)
#  '20080107~200801137': {'기간': '20080107~20080113',
#                         '기간순위': '20080107~200801137',
#                         '기간시작': '20080107',
#                         '기간종료': '20080113',
#                         '순위': '7',
#                         '영화명(국문)': '황금 나침반',
#                         '영화코드': '20070551'},

# 네이버에서 영화에 맞는 줄거리와 포스터url를 받아와서 dict에 합친 후,
# model.py의 MakeDB모델을 거쳐 우리 DB에 저장한다
fieldnames = ('기간순위', '기간', '기간시작', '기간종료', '썸네일_이미지의_URL', '영화명(국문)', '영화코드', '하이퍼텍스트_링크', '줄거리')
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
        # print('---------------')

        writer.writerow(movie_dict)

