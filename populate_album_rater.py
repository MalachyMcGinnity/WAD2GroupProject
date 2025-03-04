import os
import datetime as dt
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2GroupProject.settings')

django.setup()

from django.contrib.auth.models import User
from album_rater.models import Album, UserProfile, Comment
from django.utils.timezone import now

def add_album(title, uploader, upload_date = now(), views = 0, genre = "unknown"):
    a, created = Album.objects.get_or_create(title = title, uploader = uploader)
    if created:
        a.upload_date = upload_date
        a.views = views
        a.genre = genre
        a.save()
    return a

def add_user_profile(username, password, date_created = now()):
    user, created = User.objects.get_or_create(username = username)
    if created:
        user.password = password
        user.save()
    up, created = UserProfile.objects.get_or_create(user = user)
    if created:
        up.date_created = date_created
        up.save()
    return up

def add_comment(text, user_profile, album, score = 0):
    c, created = Comment.objects.get_or_create(text = text, user_profile = user_profile, album = album)
    if created:
        c.score = score
        c.save()
    return c

def populate():
    user_info = [("username0", "password"), ("username1", "password"), ("username2", "password"), ("username3", "password")]
    users = []
    for user in user_info:
        users.append(add_user_profile(user[0], user[1]))
    
    album_titles = [("I Don't Know Albums", "rock"), ("Nonsense", "metal"), ("Lorem Ipsum", "rap"), ("Tha mi sgith", "jazz"),
                    ("If you are reading this, good evening", "musical"), ("Tha mi an dochas gum bi sin sgoinneil", "pop"),
                    ("Last one, I swear", "unknown"), ("Kendrick Lamar's 2025 Superbowl Half-Time Show", "rap")]
    albums = []
    for i in range(len(album_titles)):
        albums.append(add_album(album_titles[i][0], users[i%4], genre = album_titles[i][1]))
    
    for i in range(len(users)):
        users[i].favourite_album = albums[(2*i + 3)%len(albums)]

        users[i].liked_albums.add(albums[(2*i + 3)%len(albums)])
        users[i].liked_albums.add(albums[(i + 6)%len(albums)])
        users[i].liked_albums.add(albums[(5*i + 1)%len(albums)])

        users[i].users_followed.add(users[(3*i + 7)%len(users)])
        users[i].users_followed.add(users[(4*i - 2)%len(users)])

        users[i].save()
    
    user_messages = ["Great Job", "kinda mid", "According to all known laws of aviation...", "A MINOOOOOOOOR", "Honestly, it sucks",
                     "Gotta love this artists work", "Did you know that Barack Obama is (as of 2025-03-03) the only US President to serve there term under the same flag they were born under?",
                     "Ma tha sin deiseil a-nochd, bidh oidhche mhath agam."]
    comments = []
    for i in range(len(users)):
        for j in range(len(users)):
            comments.append(add_comment(user_messages[(len(users)*i + j)%len(user_messages)], users[i], albums[j]))

if __name__ == "__main__":
    print("Starting Album Rater popultaion script...")
    populate()