import requests
from pprint import pprint
from decouple import config
import csv

for year in range(2004, 2019):
    with open('movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
        items = csv.DictReader(f)
        target = 1223
        
        print('year', year)
        year = year * 10000
        new_target = year + target
        print('new_target', new_target)


        for item in items:
            start = int(item['기간시작'])
            end = int(item['기간종료'])

            if start <= new_target <= end:
                rank = item['기간순위'][-1]
                title = item['영화제목']
                poster_url = item['썸네일_이미지의_URL']
                discription = item['줄거리']
                naver_movie_url = item['하이퍼텍스트_링크']
                print(rank, title, poster_url, discription, naver_movie_url)
                


# 우리가 필요한 것 : 순위, 제목, 줄거리, 썸네일 url, naver_link