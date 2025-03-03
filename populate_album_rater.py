import os
import datetime as dt
from django.contrib.auth.models import User
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from album_rater.models import Album, UserProfile, Comment

def add_album(title, uploader, upload_date = dt.date.today, views = 0, genre = "unknown"):
    a = Album.objects.get_or_create(title = title, uploader = uploader)[0]
    a.upload_date = upload_date
    a.views = views
    a.genre = genre
    a.save()
    return a

def add_user_profile(username, password, date_created = dt.date.today):
    user = User.objects.create_user(username = username, password = password)
    up = UserProfile.objects.get_or_create(user = user)[0]
    up.date_created = date_created
    up.save()
    return up

def add_comment(text, user_profile, album, score = 0):
    c = Comment.objects.get_or_create(text = text, user_profile = user_profile, album = album)[0]
    c.score = score
    c.save()
    return c

def populate():
    #First names i could think of
    user_info = [("Josh", "McPhail"), ("Malachy", "McGinnity"), ("Pavlo", "Matveiev"), ("Declan", "McLaren")]
    users = []
    for user in user_info:
        users.append(add_user_profile(user[0], user[1]))
    
    album_titles = [("I Don't Know Albums", "rock"), ("Nonsense", "metal"), ("Lorem Ipsum", "rap"), ("Tha mi sgith", "jazz"),
                    ("If you are reading this, good evening", "musical"), ("Tha mi an dochas gum bi sin sgoinneil", "pop"),
                    ("Last one, I swear", "unknown"), ("Kendrick Lamar's 2025 Superbowl Half-Time Show", "rap")]
    albums = []
    for i in range(len(album_titles)):
        albums.append(add_album(album_titles[i][0], users[i%4], genre = album_titles[i][0]))
    
    for i in range(len(users)):
        users[i].favourite_album = albums[(2*i + 3)%len(albums)]

        users[i].liked_albums.add(albums[(2*i + 3)%len(albums)])
        users[i].liked_albums.add(albums[(i + 6)%len(albums)])
        users[i].liked_albums.add(albums[(5*i + 1)%len(albums)])

        users[i].users_followed.add(users[(3*i + 7)%len(users)])
        users[i].users_followed.add(users[(4*i - 2)%len(users)])
    
    user_messages = ["Great Job", "kinda mid", "According to all known laws of aviation...", "A MINOOOOOOOOR", "Honestly, it sucks",
                     "Gotta love this artists work", "Did you know that Barack Obama is (as of 2025-03-03) the only US President to serve there term under the same flag they were born under?",
                     "Ma tha sin deiseil a-nochd, bidh oidhche mhath agam."]
    comments = []
    for i in range(len(users)):
        for j in range(len(users)):
            comments.append(user_messages[(len(users)*i + j)%len(user_messages)], users[i], albums[j])

if __name__ == "__main__":
    print("Starting Album Rater popultaion script...")
    populate()