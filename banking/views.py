from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Account
from .forms import AccountForm


@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user).order_by("-is_active", "-id")
    return render(request, "banking/account_list.html", {"accounts": accounts})


@login_required
def account_create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("account_list")
    else:
        form = AccountForm()
    return render(request, "banking/account_form.html", {"form": form, "mode": "create"})


@login_required
def account_update(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("account_list")
    else:
        form = AccountForm(instance=account)

    return render(request, "banking/account_form.html", {"form": form, "mode": "update", "account": account})


@login_required
def account_delete(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == "POST":
        account.delete()
        return redirect("account_list")

    return render(request, "banking/account_confirm_delete.html", {"account": account})