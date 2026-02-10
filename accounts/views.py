from django.contrib.auth.forms import UserCreationForm  # ✅ 추가: Django 기본 회원가입 폼
from django.contrib.auth import login                  # ✅ 추가: 가입 후 자동 로그인 처리
from django.shortcuts import render, redirect


def signup(request):
    """
    회원가입 처리 함수(뷰).

    - GET  요청: 회원가입 폼 화면을 보여줌
    - POST 요청: 사용자가 입력한 데이터로 회원가입을 시도
      - 성공하면: 유저 생성 -> 자동 로그인 -> 지출 목록(/expenses/)으로 이동
      - 실패하면: 같은 화면에 에러와 함께 폼을 다시 보여줌
    """
    if request.method == "POST":
        # ✅ 추가: 사용자가 입력한 회원가입 데이터를 폼에 담아서 검증
        form = UserCreationForm(request.POST)

        # ✅ 추가: 폼 검증(아이디 중복, 비밀번호 규칙 등)
        if form.is_valid():
            user = form.save()      # ✅ 추가: 유저 생성(DB에 저장)
            login(request, user)    # ✅ 추가: 방금 만든 유저로 로그인 처리(세션 생성)
            return redirect("expense_list")  # ✅ 추가: 지출 목록 페이지로 이동
    else:
        # ✅ 추가: 처음 페이지 들어왔을 때는 빈 폼을 보여줌
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})