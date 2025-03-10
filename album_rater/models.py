from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now

class Album(models.Model):
    MAX_TITLE_LENGTH = 40
    GENRES = [
        ("unknown", "Unknown"),
        ("rock", "Rock"),
        ("musical", "Musical Theatre"),
        ("metal", "Metal"),
        ("pop", "Pop"),
        ("jazz", "Jazz"),
        ("rap", "Rap")
    ]
    title = models.CharField(max_length = MAX_TITLE_LENGTH)
    #rating = models.FloatField(default = 0)
    art = models.ImageField(upload_to = "album_covers", blank = True)
    uploader = models.ForeignKey("UserProfile", on_delete = models.CASCADE)
    upload_date = models.DateField(default = now)
    views = models.IntegerField(default = 0)
    genre = models.CharField(max_length = 20, choices = GENRES, default = "unknown")
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_created = models.DateField(default = now)
    favourite_album = models.ForeignKey(Album, on_delete = models.CASCADE, default = None, null = True, blank = True, related_name = "favourited_by")
    #followers = models.IntegerField(default = 0)
    #following = models.IntegerField(default = 0)
    liked_albums = models.ManyToManyField(Album, related_name = "liked_by")
    users_followed = models.ManyToManyField("self", symmetrical = False)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    MAX_COMMENT_LENGTH = 255
    text = models.CharField(max_length = MAX_COMMENT_LENGTH)
    user_profile = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    album = models.ForeignKey(Album, on_delete = models.CASCADE)
    score = models.IntegerField(default = 0)

    def __str__(self):
        return self.text
