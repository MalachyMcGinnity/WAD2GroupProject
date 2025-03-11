from django.urls import path
from album_rater import views

app_name = "album-rater"

urlpatterns = [
    path('',views.index,name="index"),
    path('about/',views.about,name="about"),
    path('sign_up/',views.register,name="register"),
    path('log_in/',views.user_login,name="log_in"),
    path('log_out/',views.user_logout,name="log_out"),
    path('upload/',views.upload,name="upload"),
    path('delete_account/',views.delete_account,name="delete_account"),
    path('profile/<slug:username_slug>',views.profile,name="user_profile"),
    path('album/<slug:album_name>',views.album,name="album"),
    path('charts/',views.charts,name="charts"),
    path('change_password',views.change_password,name="change_password"),
]