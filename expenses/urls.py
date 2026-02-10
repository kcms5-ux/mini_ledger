from django.urls import path
from . import views

urlpatterns = [
    # /expenses/
    path("", views.expense_list, name="expense_list"),

    # /expenses/new/
    path("new/", views.expense_create, name="expense_create"),

    # ✅ /expenses/3/
    path("<int:expense_id>/", views.expense_detail, name="expense_detail"),

    # /expenses/3/edit/
    path("<int:expense_id>/edit/", views.expense_update, name="expense_update"),

    # /expenses/3/delete/
    path("<int:expense_id>/delete/", views.expense_delete, name="expense_delete"),
]