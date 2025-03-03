from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Album(models.Model):
    MAX_TITLE_LENGTH = 40
    GENRES = [
        ("unknown", "Unknown"),
        ("rock", "Rock"),
        ("musical", "Musical Theatre"),
        ("metal", "Metal")
    ]
    title = models.CharField(max_length = MAX_TITLE_LENGTH)
    rating = models.FloatField(default = 0)
    art = models.ImageField(upload_to = "album_covers", blank = True)
    uploader = models.ForeignKey("UserProfile", on_delete = models.CASCADE)
    upload_date = models.DateField(default = dt.date.today)
    views = models.IntegerField(default = 0)
    genre = models.CharField(max_length = 20, choices = GENRES, default = "unknown")
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_created = models.DateField(default = dt.date.today)
    favourite_album = models.ForeignKey(Album, on_delete = models.CASCADE)
    followers = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)
    liked_albums = models.ManyToManyField(Album)
    users_followed = models.ManyToManyField("self", symmetrical = False)

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    MAX_COMMENT_LENGTH = 255
    text = models.CharField(max_length = MAX_COMMENT_LENGTH)
    username = models.ForeignKey(UserProfile)
    album_id = models.ForeignKey(Album, on_delete = models.CASCADE)
    score = models.IntegerField(default = 0)

    def __str__(self):
        return self.text
