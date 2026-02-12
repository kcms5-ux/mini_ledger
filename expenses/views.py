# 기능 모음

from __future__ import annotations
from datetime import date
import calendar

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-spent_at", "-id")

    category = request.GET.get("category", "").strip()
    q = request.GET.get("q", "").strip()
    date_from = request.GET.get("from", "").strip()
    date_to = request.GET.get("to", "").strip()
    min_amount = request.GET.get("min", "").strip()
    max_amount = request.GET.get("max", "").strip()

    if category:
        expenses = expenses.filter(category=category)
    if q:
        expenses = expenses.filter(memo__icontains=q)
    if date_from:
        expenses = expenses.filter(spent_at__gte=date_from)
    if date_to:
        expenses = expenses.filter(spent_at__lte=date_to)
    if min_amount:
        try:
            expenses = expenses.filter(amount__gte=int(min_amount))
        except ValueError:
            pass
    if max_amount:
        try:
            expenses = expenses.filter(amount__lte=int(max_amount))
        except ValueError:
            pass

    categories = Expense.Category.choices

    return render(
        request,
        "expenses/list.html",
        {
            "expenses": expenses,
            "categories": categories,
            "filter": {"category": category, "q": q, "from": date_from, "to": date_to, "min": min_amount, "max": max_amount},
        },
    )


def _shift_month(year: int, month: int, delta_months: int) -> tuple[int, int]:
    m = (year * 12 + (month - 1)) + delta_months
    new_year = m // 12
    new_month = (m % 12) + 1
    return new_year, new_month


@login_required
def dashboard(request):
    """
    ✅ JS 없는 그래프 대시보드 (막대 그래프)
    - KPI: 총수입/총지출/순합/건수 (원 단위, 콤마는 템플릿에서 intcomma)
    - 카테고리별 지출 비중: 가로 컬러 막대 (원 단위 표기 유지)
    - 최근 6개월 지출/일별 지출: 값 표시를 만원 단위(반올림)로 변경 -> 겹침 방지
      예) 2,573,123원 -> 257만원
    """
    month_str = request.GET.get("month", "").strip()
    today = date.today()

    if month_str:
        try:
            year, month = month_str.split("-")
            year = int(year)
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            year = today.year
            month = today.month
    else:
        year = today.year
        month = today.month

    last_day = calendar.monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, last_day)

    month_qs = Expense.objects.filter(user=request.user, spent_at__range=(start, end))

    in_total = month_qs.filter(tx_type=Expense.TxType.IN).aggregate(total=Sum("amount")).get("total") or 0
    out_total = month_qs.filter(tx_type=Expense.TxType.OUT).aggregate(total=Sum("amount")).get("total") or 0
    net = int(in_total) - int(out_total)
    tx_count = month_qs.aggregate(cnt=Count("id")).get("cnt") or 0

    # 지출(OUT) 기준 시각화
    out_qs = month_qs.filter(tx_type=Expense.TxType.OUT)

    palette = [
        "#2563eb",  # blue
        "#16a34a",  # green
        "#f59e0b",  # amber
        "#ef4444",  # red
        "#8b5cf6",  # violet
        "#06b6d4",  # cyan
        "#111827",  # slate
    ]

    # 1) 카테고리별 지출 합계 + 퍼센트 (가로 막대)
    category_rows = (
        out_qs.values("category")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )
    label_map = dict(Expense.Category.choices)

    category_items = []
    out_total_int = int(out_total) or 0

    for idx, r in enumerate(category_rows):
        total = int(r["total"] or 0)
        pct = (total / out_total_int * 100) if out_total_int else 0
        category_items.append({
            "label": label_map.get(r["category"], r["category"]),
            "total": total,
            "pct": round(pct, 1),
            "count": int(r["count"] or 0),
            "color": palette[idx % len(palette)],
        })

    # 2) 최근 6개월 월별 지출(OUT) 세로 막대
    start_y, start_m = _shift_month(year, month, -5)
    range_start = date(start_y, start_m, 1)
    range_end = end

    range_out_qs = Expense.objects.filter(
        user=request.user,
        tx_type=Expense.TxType.OUT,
        spent_at__range=(range_start, range_end),
    )

    month_bucket = {}
    for row in range_out_qs.values("spent_at", "amount"):
        ym = row["spent_at"].strftime("%Y-%m")
        month_bucket[ym] = month_bucket.get(ym, 0) + int(row["amount"])

    trend_items = []
    trend_values = []

    for i in range(-5, 1):
        y, m = _shift_month(year, month, i)
        ym = f"{y:04d}-{m:02d}"
        total = int(month_bucket.get(ym, 0))

        trend_values.append(total)
        trend_items.append({
            "ym": ym,
            "total": total,
            "total_man": int(round(total / 10000)),  # ✅ 만원 단위(반올림)
        })

    trend_max = max(trend_values) if trend_values else 0

    for idx, item in enumerate(trend_items):
        item["bar_pct"] = round((item["total"] / trend_max * 100), 1) if trend_max else 0
        item["color"] = palette[idx % len(palette)]

    # 3) 일별 지출(OUT) 세로 막대 (스크롤)
    daily_rows = (
        out_qs.values("spent_at")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("spent_at")
    )

    daily_values = [int(r["total"] or 0) for r in daily_rows]
    daily_max = max(daily_values) if daily_values else 0

    daily_items = []
    for r in daily_rows:
        total = int(r["total"] or 0)
        daily_items.append({
            "date": r["spent_at"],
            "total": total,
            "total_man": int(round(total / 10000)),  # ✅ 만원 단위(반올림)
            "count": int(r["count"] or 0),
            "bar_pct": round((total / daily_max * 100), 1) if daily_max else 0,
        })

    return render(
        request,
        "dashboard.html",
        {
            "selected_month": f"{year:04d}-{month:02d}",
            "month_label": f"{year}년 {month}월",
            "range": {"start": start, "end": end},
            "kpi": {
                "in_total": int(in_total),
                "out_total": int(out_total),
                "net": int(net),
                "count": int(tx_count),
            },
            "category_items": category_items,
            "trend_items": trend_items,
            "daily_items": daily_items,
        },
    )


@login_required
def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    return render(request, "expenses/detail.html", {"expense": expense})


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(user=request.user)

    return render(request, "expenses/new.html", {"form": form})


@login_required
def expense_update(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("expense_detail", expense_id=expense.id)
    else:
        form = ExpenseForm(instance=expense, user=request.user)

    return render(request, "expenses/edit.html", {"form": form, "expense": expense})


@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")

    return redirect("expense_list")