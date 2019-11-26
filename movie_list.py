import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
key = config('API_KEY')
weekGb = '0'

with open('movie.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['순위', '기간', '영화코드', '영화명(국문)', '기간순위', '기간시작', '기간종료']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1000):
        targetDt = datetime(2019, 11, 17) - timedelta(weeks=i)
        targetDt = targetDt.strftime('%Y%m%d')
        API_URL = f'{BASE_URL}?key={key}&targetDt={targetDt}&weekGb=0'

        response = requests.get(API_URL)
        data = response.json()
        movie_data = {}

        showRange = data['boxOfficeResult']['showRange']
        # start_date, end_date가 2003-01-01 형태(날짜형태)로 들어왔다
        start = showRange[:4] + '-' + showRange[4:6] + '-' + showRange[6:8]
        end = showRange[9:13] + '-' + showRange[13:15] + '-' + showRange[15:17]
        # print(start)
        # print(end)

        for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
            # pprint(movie)
            movie_data[movie.get('movieCd')] = {
                '기간순위': showRange + movie.get('rank'),
                '기간': showRange,
                '기간시작': start,
                '기간종료': end,
                '영화코드': movie.get('movieCd'),
                '영화명(국문)': movie.get('movieNm'),
                '순위': movie.get('rank'),
            }

        for item in movie_data.values():
            writer.writerow(item)
