from django.contrib import admin
from django.urls import path
from django.urls import include
from dailydoodle import views

app_name = "dailydoodle"

urlpatterns = [
    path("",views.Index.as_view(),name="index"),
]
