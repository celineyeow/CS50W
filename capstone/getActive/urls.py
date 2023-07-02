from django import VERSION
from django.urls import path

from . import views

urlpatterns = [
    path("", views.activities, name="activities"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_activity/<int:type>", views.new_activity, name="new_activity"),
    path("activity/<str:title>", views.activity, name="activity"),
    path("my_activities", views.my_activities, name="my_activities"),
    path("filter_activities/<int:page>", views.filter_activities, name="filter_activities"),
    path("enroll/<str:title>", views.enroll, name="enroll"),
    path("get_enrrolled_activities", views.get_enrrolled_activities, name="get_enrrolled_activities")
]
