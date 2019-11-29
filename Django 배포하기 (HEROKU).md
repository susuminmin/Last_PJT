# Django 배포하기 (HEROKU)



0. 가상환경 잡기

1. heroku라는 브랜치 따기
   `git checkout -b 'heroku'`

2. `pip install django-heroku`
   : 장고가 헤로쿠에 잘 배포될 수 있도록 내부적으로 환경을 설정해주는 라이브러리
   : 설치만 해주면 되고, 따로 뭔가 설정할 필요는 없다

3. `Procfile`이라는 파일 만들기
   : 웹 어플리케이션이 헤로쿠에서 구독도리 때, 실행되는 프로세스를 정의하는 곳
   `$ vi Procfile`

   ```bash
   web: gunicorn lastpjt.wsgi --log-file -  입력
   ```

   gunicorn : 서버같은 역할

4. gunicorn 깔아주기 &  requirements 파일 만들기
    `pip install gunicorn`  
    `$ pip freeze > requirements.txt`

  - 혹시 pywin , aws~  파일이 있다면 삭제해주기

5. `runtime.txt`파일 만든 후, python-3.7.4 작성

6. lastpjt // settings 환경설정

   - STATIC_ROOT 설정
   - SECRET_KEY / DEBUG  -> env설정

7. 헤로쿠 홈페이지 -> ` https://devcenter.heroku.com/articles/heroku-cli ` 들어오기
   : 검색에서 heroku cli 검색 후, 두번째 탭 -> gerodu.cli 클릭
   windows-64bit 다운

8. vscode 모두 다 껐다가 킨 후, heroku라고 쳤을 때, 인식하면 정상적으로 설치된 것

9. `heroku login` -> 새로 켜진 브라우저에서 로그인버튼 클릭 -> 다시 vscode로 돌아오기

10. `$ heroku create sue-ssung-project` 프로젝트 이름 정해주기

11. 헤로쿠 셋팅

    - 헤로쿠 홈페이지 -> 우리가 만든 서버가 나옴
    - settings -> config vars 에서 Reveal Config Vars 클릭 -> SETCRET_KEY , DEBUG value 입력
12. git bash로 와서
    - git add . / git commit / `$ git push heroku heroku:master` (우리는 지금 heroku 브랜치인데, heroku라는 이름으로 master 브랜치에 올리겠다)

​    



  

