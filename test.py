import os
import django
from django.db import transaction

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lastpjt.settings")
django.setup()
# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from movies.models import Movie


@transaction.atomic
def make_model():
    movie = Movie()

    movie.range_rank = '7'
    movie.showRange = '20191111~201911171'
    movie.poster_url = 'www.naver.com'
    movie.title = '쑤하'
    movie.movie_code = 20191234
    movie.naver_movie_url = 'www.google.com'
    movie.description = '대니’(나탈리아 레이즈)를 지키기 위해 슈'
    movie.save()


if __name__ == "__main__":
    make_model()