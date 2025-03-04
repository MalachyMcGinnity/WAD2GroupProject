from django.urls import path
from album_rater import views

app_name = "album-rater"

urlpatterns = [
    path("account/register/", views.test_register, name = "register"),
    path("album/create", views.add_album, name = "create-album"),
    path("index/", views.index, name = "index")
]