import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'

DETAIL_BASE_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

key = config('API_KEY')
weekGb = '0'

with open('movie.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['순위', '기간', '영화코드', '영화명(국문)', '기간순위', '기간시작', '기간종료', '개봉일', '감독명(국문)', '감독명(영문)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1000):
        targetDt = datetime(2019, 11, 17) - timedelta(weeks=i)
        targetDt = targetDt.strftime('%Y%m%d')
        API_URL = f'{BASE_URL}?key={key}&targetDt={targetDt}&weekGb=0&itemPerPage=4'

        response = requests.get(API_URL)
        data = response.json()
        movie_data = {}
        # pprint(data)
        showRange = data['boxOfficeResult']['showRange']
        start = int(showRange[:8])
        end = int(showRange[9:])

        for movie in data['boxOfficeResult']['weeklyBoxOfficeList']:
            movieCd = movie.get('movieCd')
            API_DETAIL_URL = f'{DETAIL_BASE_URL}?key={key}&movieCd={movieCd}'
            det_response = requests.get(API_DETAIL_URL)
            det_data = det_response.json()
            # pprint(det_data)
            try:
                director = det_data['movieInfoResult']['movieInfo']['directors'][0]['peopleNm']
            except:
                pass
            try:
                directorEn = det_data['movieInfoResult']['movieInfo']['directors'][0]['peopleNmEn']
            except:
                pass

            movie_data[movie.get('movieCd')] = {
                '기간순위': showRange + movie.get('rank'),
                '기간': showRange,
                '기간시작': start,
                '기간종료': end,
                '영화코드': movie.get('movieCd'),
                '영화명(국문)': movie.get('movieNm'),
                '순위': movie.get('rank'),
                '개봉일': movie.get('openDt'),
                '감독명(국문)': director,
                '감독명(영문)': directorEn,
            }

        for item in movie_data.values():
            writer.writerow(item)
