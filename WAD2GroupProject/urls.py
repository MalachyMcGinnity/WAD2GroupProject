from django.contrib import admin
from django.urls import path
from django.urls import include
from album_rater import views

urlpatterns = [
    path("", views.index, name = "index"),
    path('admin/', admin.site.urls, name = "admin"),
    path("album-rater/", include("album_rater.urls"))
]
