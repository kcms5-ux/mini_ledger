# 기능 모음

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    """
    지출 목록 페이지: /expenses/
    - 내 지출만 조회
    """
    expenses = Expense.objects.filter(user=request.user).order_by("-spent_at", "-id")
    return render(request, "expenses/list.html", {"expenses": expenses})


@login_required
def expense_detail(request, expense_id):
    """
    ✅ 지출 상세 페이지: /expenses/<id>/
    - 내 지출만 조회 가능(user=request.user 필터)
    """
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    return render(request, "expenses/detail.html", {"expense": expense})


@login_required
def expense_create(request):
    """
    지출 추가 페이지: /expenses/new/
    - POST 시 user를 현재 로그인 유저로 강제 지정
    """
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()

    return render(request, "expenses/new.html", {"form": form})


@login_required
def expense_update(request, expense_id):
    """
    지출 수정 페이지: /expenses/<id>/edit/
    - 내 지출만 수정 가능
    """
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_detail", expense_id=expense.id)  # ✅ 변경: 수정 후 상세로 이동
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "expenses/edit.html", {"form": form, "expense": expense})


@login_required
def expense_delete(request, expense_id):
    """
    지출 삭제: /expenses/<id>/delete/
    - POST로만 삭제
    - 내 지출만 삭제 가능
    """
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")

    return redirect("expense_list")