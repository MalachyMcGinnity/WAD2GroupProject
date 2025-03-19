from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from album_rater import views

urlpatterns = [
    path("", views.index, name = "index"),
    path('admin/', admin.site.urls, name = "admin"),
    path("album-rater/", include("album_rater.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
