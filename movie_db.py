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

    movie.range_rank = 
    movie.showRange = 
    movie.poster_url = 
    movie.title = 
    movie.movie_code = 
    movie.naver_movie_url = 
    movie.description = 
    movie.save()


if __name__ == "__main__":
    make_model()