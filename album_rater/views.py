from django.shortcuts import render
from django.http import HttpResponse
from album_rater.models import Album, UserProfile, Comment
from album_rater.forms import AlbumForm, UserForm, UserProfileForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
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

    return render(request, 'index.html', context=context_dict)

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
                  'album_rater/SignUp.html',
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
                return redirect(reverse('album_rater:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:

            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'album_rater/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('album_rater:index'))

@login_required
def user_change_password(request):
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

@login_required
def user_delete_account(request):
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
            return redirect('album_rater:index')
        else:
            messages.error(request, "Password is incorrect")

    return render(request, 'delete_account.html')

