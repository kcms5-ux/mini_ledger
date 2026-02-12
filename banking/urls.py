from django.urls import path
from . import views

urlpatterns = [
    path("", views.account_list, name="account_list"),
    path("new/", views.account_create, name="account_create"),
    path("<int:account_id>/edit/", views.account_update, name="account_update"),
    path("<int:account_id>/delete/", views.account_delete, name="account_delete"),
]