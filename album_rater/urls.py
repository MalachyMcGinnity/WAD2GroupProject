from django.urls import path
from album_rater import views

app_name = "album-rater"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('accounts/register/', views.account_register, name="register"),
    path('accounts/login/', views.account_login, name="login"),
    path('accounts/logout/', views.account_logout, name="logout"),
    path('accounts/password-change/', views.account_password_change, name="password_change"),
    path('accounts/delete-account/', views.account_delete, name="delete_account"),
    path('user/<str:username>/', views.profile, name="user_profile"),
    path('album/<slug:album_slug>/', views.album, name="album_detail"),
    path('album/create/', views.album_create, name="album_create"),
    path('search/', views.search, name="search"),
    # AJAX endpoints
    path('ajax/rate_album/', views.ajax_rate_album, name="ajax_rate_album"),
    path('ajax/follow_user/', views.ajax_follow_user, name="ajax_follow_user"),
    path('ajax/comment_album/', views.ajax_comment_album, name="ajax_comment_album"),
]