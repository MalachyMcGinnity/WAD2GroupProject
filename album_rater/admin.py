from django.contrib import admin
from album_rater.models import Album, Comment, UserProfile

admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(UserProfile)