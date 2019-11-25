from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def signup(request):  # 사용자에게 Form 제공해야 함
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        # 회원가입 로직
        form = UserCreationForm(request.POST)
        if form.is_valid():  # 잘 입력 되었는지 확인
            user = form.save()
            auth_login(request, user)  # 자동 로그인 기능
            # form.save()
            return redirect('movies:index')
    else:  # GET
        # 회원가입 페이지 보여주기
        # Form 을 context 에 담아서
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# 세션 데이터 만들기
# @login_required : GET 요청에서만 사용하면 됨 / 그러나 delete는 POST 라서 쓸 수 없음 // create, update는 GET 요청을 통해 그 페이지로 이동 ==> 그렇기 때문에 그 페이지로 이동하고자 할 때 login_required 사용되는 것
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        # 로그인 로직
        if form.is_valid():
            next_page = request.GET.get('next')  # url 붙은 str 꺼낼 때
            auth_login(request, form.get_user())  # 여기에만 request 들어간다
            # next 있으면 그 페이지로 보내고 아니면 index 페이지로 보내라 (중요!)
            # redirect 는 GET 요청만 지원 (주소창에 엔터치는 것과 동일한 일)
            return redirect(next_page or 'movies:index')
    else:
        # 로그인 = 세션 데이터 만드는 것 => UserCreationForm 사용 X AuthenticationForm 사용 O
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# 세션 정보 삭제
def logout(request):
    # POST, GET 구분 불필요
    auth_logout(request)
    return redirect('movies:index')


# from django.views.decorators.http import require_POST, require_GET 추가 후
# @require_POST
# def delete(request):
#     request.user.delete()
#     return redirect('movies:index')


# @login_required
# def update(request):  # 로그아웃 상태에서 들어가면 'AnonymousUser' object has no attribute '_meta'
#     if request.method == "POST": # 별도 페이지 필요한 경우: 1)POST, 2)GET 두 가지로 분기
#         # 1) 수정 요청 들어올 때
#         form = UserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('movies:index')
#     else:  # GET
#         # 2) 수정할 페이지 요청 들어올 때
#         form = UserChangeForm(instance=request.user)  # 비어있는 폼 보냄
#     context = {'form': form}
#     return render(request, 'accounts/update.html', context)


# @login_required
# def password(request):  
#     if request.method == "POST":
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return redirect('accounts:update')
#     else:  # GET
#         form = PasswordChangeForm(request.user)  # 함수 원래 모습 보면 user 가 첫 번째 인자임
#     context = {'form': form}
#     return render(request, 'accounts/password.html', context)