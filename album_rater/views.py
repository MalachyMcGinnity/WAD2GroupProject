from django.shortcuts import render
from django.http import HttpResponse
from album_rater.models import Album, UserProfile, Comment
from album_rater.forms import AlbumForm, UserForm, UserProfileForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def get_followed_rated_albums(request):
    try:
        followed = UserProfile.objects.get(user = request.user).users_followed.all()
        albums = set()
        for follower in followed:
            for album in follower.liked_album.all():
                albums.add(album)
                if len(albums) >= 5:
                    break
            if len(albums) >= 5:
                break
        return list(albums)
    except:
        return set()

def index(request):
    album_list = Album.objects
    user_profile_list = UserProfile.objects
    comment_list = Comment.objects

    context_dict = {}
    context_dict['albums'] = album_list
    context_dict['userprofiles'] = user_profile_list
    context_dict['comments'] = comment_list
    context_dict["popular_albums"] = album_list.order_by("-views")[:5]
    context_dict["albums_rated_by_followed"] = get_followed_rated_albums(request)
    context_dict["recent_albums"] = album_list.order_by("-upload_date")[:5]

    visitor_cookie_handler(request)
    visits = request.session.get('visits', 1)

    return render(request, 'album_rater/index.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            profile.save()

            registered = True

            login(request, user)
            return redirect(reverse("album-rater:index"))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'album_rater/register.html',
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
                return redirect(reverse('album-rater:index'))
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
    return redirect(reverse('album-rater:index'))

def about(request):
    return render(request, 'album_rater/about.html')

def upload(request):
    #stub view
    return render(request, 'album_rater/upload.html')

def delete_account(request):
    if request.method == 'POST':
        confirm_username = request.POST.get('confirmUsername')
        password = request.POST.get('password')

        if confirm_username != request.user.username:
            messages.error(request, "The username doesn't mactch the account.")
            return render(request, 'delete_account.html')
        
        user = authenticate(username=request.user.username, password=password)

        if user:
            user.delete()
            logout(request)
            messages.success(request, "Account deleted")
            return redirect('album-rater:index')
        else:
            messages.error(request, "Password is incorrect")

    return render(request, 'delete_account.html')

def profile(request, username_slug):
    #stub view
    context_dict = {"username": username_slug}
    return render(request, 'album_rater/profile.html')

def album(request, album_name):
    #stub view
    context_dict = {"album": Album.objects.get(slug = album_name)}
    comments = Comment.objects.filter(album = context_dict["album"])
    context_dict["score"] = round(0 if len(comments) == 0 else sum(comment.score for comment in comments)/len(comments), 1)
    context_dict["comments"] = comments
    context_dict["genre"] = context_dict["album"].get_genre_display()
    context_dict["date"] = context_dict["album"].upload_date.strftime("%B %d, %Y")
    return render(request, 'album_rater/album.html', context = context_dict)

def charts(request):
    #stub view
    return render(request, 'album_rater/search.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmNewPassword')

        if new_password and confirm_password:
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Your password has been updated.")
                return redirect('album_rater:index')
            else:
                messages.error(request, "Passwords do not match, please try again.")
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'change_password.html')

def visitor_cookie_handler(request):
    pass
