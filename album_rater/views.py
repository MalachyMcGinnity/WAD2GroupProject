from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from album_rater.forms import UserForm, UserProfileForm, AlbumForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def test_register(request):
    #View for a user to register
    registered = False #flag

    if request.method == "POST":
        #Grab info from the raw form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Hash the password, then update the object
            user.set_password(user.password)
            user.save()

            #Dont commit profile yet
            profile = profile_form.save(commit = False)
            profile.user = user #set user

            #Search for input image
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            
            #Save, and complete registration
            profile.save()
            registered = True
        else:
            #Invalid, print issues to command
            print(user_form.errors, profile_form.errors)
    else:
        #Not an HTTP POST, render with blank forms
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    #Render with context
    context_dict = {"forms": [user_form, profile_form], "file": reverse("album-rater:register")}
    return render(request, "album_rater/test_form.html", context_dict)

def add_album(request):
    form = AlbumForm()

    if request.method == "POST":
        form = AlbumForm(request.POST)

        if form.is_valid():
            album = form.save()

            if "art" in request.FILES:
                album.art = request.FILES["art"]
            print(User.objects.get(username = "josh"))
            album.uploader = User.objects.get(username = "josh")

            album.save()

            #Redirect user back to the index view
            return redirect(reverse("album-rater:index"))
        else:
            #Invalid
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    return render(request, "album_rater/test_form.html", {"forms": [form], "file": reverse("album-rater:create-album")})

def index(request):
    return render(request, "album_rater/index.html")