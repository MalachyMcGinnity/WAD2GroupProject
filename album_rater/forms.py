from django import forms
from album_rater.models import Album, UserProfile, Comment
from django.contrib.auth.models import User

class AlbumForm(forms.ModelForm):
    title = forms.CharField(label = "Album Title", max_length = Album.MAX_TITLE_LENGTH, help_text = "Please enter album title")
    art = forms.ImageField(label = "Album Cover", required = False)
    genre = forms.ChoiceField(label = "Music Genre", choices = Album.GENRES, help_text = "Please enter music genre")

    class Meta:
        model = Album
        fields = ("title", "art", "genre", "uploader")

class UserForm(forms.ModelForm):
    #username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

class CommentForm(forms.ModelForm):
    username = forms.CharField(help_text = "Enter text here.")

    class Meta:
        model = Comment
        fields = ("text", )