from django.contrib import admin
from django.urls import path
from django.urls import include
from album_rater import views

urlpatterns = [
    path('', include('album_rater.urls')),
    path('admin/', admin.site.urls),
]
