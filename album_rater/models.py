from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db.models import Avg, Q

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
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    art = models.ImageField(upload_to="album_covers", blank=True)
    uploader = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    upload_date = models.DateField(default=now)
    views = models.IntegerField(default=0)
    genre = models.CharField(max_length=20, choices=GENRES, default="unknown")
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=now)
    favourite_album = models.ForeignKey(
        Album, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="favourited_by"
    )
    liked_albums = models.ManyToManyField(Album, related_name="liked_by")
    users_followed = models.ManyToManyField("self", symmetrical=False)
    picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, default="This user hasn't provided a description yet.")

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    text = models.TextField(validators=[MaxLengthValidator(1500)])
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(default=0)
    rating_value = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        if self.rating_value:
            return f"{self.text} (Rating: {self.rating_value})"
        return self.text
