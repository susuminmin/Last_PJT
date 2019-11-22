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

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    items = csv.DictReader(f)
    # print(items)

    for item in items:
        query_dict[item['영화제목']] = {'영화코드': item['영화코드']}
        # print(query_dict)

for movie_title, movie_code in query_dict.items():
    API_URL = f'{BASE_URL}?query={movie_title}'
    response = requests.get(API_URL, headers=HEADERS).json()
    # pprint(response)
    if response.get('items')[0].get('link') == '':
        continue
    movie_code.update(영화_썸네일_이미지의_URL=response.get('items')[0].get('image'))
    hytext = response.get('items')[0].get('link')
    # print('1,', hytext)  /  link만 따옴

    hyp_link = requests.get(hytext)
    # print(hyp_link.status_code)  /  200 -> 요청이 제대로 가짐
    # print('2', hyp_link)  /  200 -> 요청이 제대로 가짐
    html = hyp_link.text  # 응답받은 객체에서 html문서를 string으로 바꾸는 것
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # print(soup)
    discription = soup.select('div.story_area p.con_tx')
    print(discription)




