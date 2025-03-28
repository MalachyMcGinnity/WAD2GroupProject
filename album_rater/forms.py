from django import forms
from album_rater.models import Album, UserProfile, Comment
from django.contrib.auth.models import User

class AlbumForm(forms.ModelForm):
    title = forms.CharField(
        label="Album Title",
        max_length=Album.MAX_TITLE_LENGTH,
        help_text="Please enter album title"
    )
    art = forms.ImageField(label="Album Cover", required=False)
    genre = forms.ChoiceField(
        label="Music Genre",
        choices=Album.GENRES,
        help_text="Please enter music genre"
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        required=False,
        help_text="Enter album description"
    )

    class Meta:
        model = Album
        fields = ("title", "art", "genre", "description")

class UserForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password")

class UserProfileForm(forms.ModelForm):
    # Form for updating user profile (bio and picture)
    bio = forms.CharField(
        label="Profile Description",
        widget=forms.Textarea,
        required=False,
        help_text="Tell us about yourself"
    )

    class Meta:
        model = UserProfile
        fields = ("picture", "bio")

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label="Comment",
        help_text="Maximum 1500 characters.",
        error_messages={'required': "Please enter your comment."}
    )
    rating_value = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 11)],
        label="Rating (1-10)",
        coerce=int
    )

    class Meta:
        model = Comment
        fields = ("text", "rating_value", )

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        normalized_text = text.replace('\r\n', '\n')
        if len(normalized_text) > 1500:
            raise forms.ValidationError(
                f"Ensure this value has at most 1500 characters (it has {len(normalized_text)})."
            )
        return normalized_text
