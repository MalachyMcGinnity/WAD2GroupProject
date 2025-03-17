from django.contrib import admin
from django.urls import path
from django.urls import include
from album_rater import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include(('album_rater.urls', 'album_rater'), namespace='album_rater')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
