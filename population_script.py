import os
import datetime as dt
import django
import random
from django.core.files import File

# === Constants for customizing database filling ===
NUM_USERS = 10                   # Number of users
ALBUMS_PER_USER = 10             # Number of albums per user
COMMENTS_PER_ALBUM = 10          # Number of comments under each album
# ===========================================================================

# List of test images (used for both covers and avatars)
TEST_PICTURES = ["TestPicture1.jpg", "TestPicture2.jpeg", "TestPicture3.jpg"]
TEST_PICTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "TestPictures")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2GroupProject.settings')
django.setup()

from django.contrib.auth.models import User
from album_rater.models import Album, UserProfile, Comment
from django.utils.timezone import now

def add_album(title, uploader, upload_date=now(), views=0, genre="unknown"):
    a, created = Album.objects.get_or_create(title=title, uploader=uploader)
    if created:
        a.upload_date = upload_date
        a.views = views
        a.genre = genre
        # Select a picture from TEST_PICTURES cyclically
        pic_filename = TEST_PICTURES[hash(title) % len(TEST_PICTURES)]
        pic_path = os.path.join(TEST_PICTURES_PATH, pic_filename)
        if os.path.exists(pic_path):
            with open(pic_path, "rb") as f:
                a.art.save(pic_filename, File(f), save=False)
        a.save()
    return a

def add_user_profile(username, password, date_created=now()):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
    up, created = UserProfile.objects.get_or_create(user=user)
    if created:
        up.date_created = date_created
        # Assign avatar from TEST_PICTURES cyclically
        pic_filename = TEST_PICTURES[hash(username) % len(TEST_PICTURES)]
        pic_path = os.path.join(TEST_PICTURES_PATH, pic_filename)
        if os.path.exists(pic_path):
            with open(pic_path, "rb") as f:
                up.picture.save(pic_filename, File(f), save=False)
        up.save()
    return up

def add_comment(text, user_profile, album, score=0):
    c, created = Comment.objects.get_or_create(text=text, user_profile=user_profile, album=album)
    if created:
        c.score = score
        # Assign a random rating from 1 to 10
        c.rating_value = random.randint(1, 10)
        c.save()
    return c

def populate():
    # Create users
    users = []
    for i in range(NUM_USERS):
        username = f"username{i}"
        password = "password"
        users.append(add_user_profile(username, password))

    # Create albums: ALBUMS_PER_USER for each user
    albums = []
    genres = ["rock", "metal", "rap", "jazz", "musical", "pop", "unknown", "rap"]
    for user in users:
        for j in range(ALBUMS_PER_USER):
            title = f"{user.user.username}'s Album {j+1}"
            genre = genres[j % len(genres)]
            album = add_album(title, user, genre=genre)
            albums.append(album)

    # For each album, create COMMENTS_PER_ALBUM comments from users (not the creator)
    user_messages = [
        "Great Job", "kinda mid", "According to all known laws of aviation...",
        "A MINOOOOOOOOR", "Honestly, it sucks", "Gotta love this artist's work",
        "Did you know that Barack Obama is the only US President to serve their term under the same flag they were born under?",
        "Ma tha sin deiseil a-nochd, bidh oidhche mhath agam."
    ]
    for album in albums:
        for i in range(COMMENTS_PER_ALBUM):
            commenters = [u for u in users if u != album.uploader]
            if commenters:
                user_profile = commenters[i % len(commenters)]
                text = user_messages[i % len(user_messages)]
                add_comment(text, user_profile, album)

if __name__ == "__main__":
    print("Starting Album Rater population script...")
    populate()
