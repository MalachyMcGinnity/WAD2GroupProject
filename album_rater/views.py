from django.shortcuts import render
from django.http import HttpResponse
from album_rater.models import Album, UserProfile, Comment
from album_rater.forms import AlbumForm, UserForm, UserProfileForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    album_list = Album.objects
    user_profile_list = UserProfile.objects
    comment_list = Comment.objects

    context_dict = {}
    context_dict['albums'] = album_list
    context_dict['userprofiles'] = user_profile_list
    context_dict['comments'] = comment_list

    visitor_cookie_handler(request)
    visits = request.session.get('visits', 1)

    return render(request, 'album_rater/index.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()


            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'album_rater/sign_up.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:

                login(request, user)
                return redirect(reverse('WAD2GroupProject:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:

            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'album_rater/log_in.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('WAD2GroupProject:index'))

def about(request):
    return render(request, 'album_rater/about.html')

def upload(request):
    #stub view
    return render(request, 'album_rater/upload.html')

def delete_account(request):
    #stub view
    return render(request, 'album_rater/delete_account.html')

def profile(request):
    #stub view
    return render(request, 'album_rater/profile.html')

def album(request):
    #stub view
    return render(request, 'album_rater/album.html')

def charts(request):
    #stub view
    return render(request, 'album_rater/search.html')

def change_password(request):
    #stub view
    return render(request, 'album_rater/change_password.html')

def visitor_cookie_handler(request):
    pass
