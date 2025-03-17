from django.urls import path
from album_rater import views

app_name = "album_rater"

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index_index"),
    path('about/', views.about, name="about"),
    path('account/register/', views.account_register, name="register"),
    path('account/login/', views.account_login, name="login"),
    path('account/logout/', views.account_logout, name="logout"),
    path('account/password-change/', views.account_password_change, name="password_change"),
    path('account/delete-account/', views.account_delete, name="delete_account"),
    path('account/edit/', views.edit_profile, name="edit_profile"),
    path('album/create/', views.album_create, name="album_create"),
    path('album/<slug:album_slug>/edit/', views.edit_album, name="edit_album"),
    path('album/<slug:album_slug>/delete/', views.delete_album, name="delete_album"),
    path('album/<slug:album_slug>/', views.album, name="album_detail"),
    path('user/<str:username>/', views.profile, name="user_profile"),
    path('search/', views.search, name="search"),
]
