from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from album_rater.models import Album, UserProfile, Comment
from album_rater.forms import AlbumForm, UserForm, UserProfileForm, CommentForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

def index(request):
    top_rated_albums = Album.objects.annotate(avg_rating=Avg('ratings__rating_value')).order_by('-avg_rating')[:5]
    today = date.today()
    todays_albums_list = Album.objects.filter(upload_date=today)
    paginator = Paginator(todays_albums_list, 18)
    page_todays = request.GET.get('page_todays')
    try:
        todays_albums = paginator.page(page_todays)
    except PageNotAnInteger:
        todays_albums = paginator.page(1)
    except EmptyPage:
        todays_albums = paginator.page(paginator.num_pages)

    followed_albums = None
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        followed_users = user_profile.users_followed.all()
        followed_albums = Album.objects.filter(ratings__user_profile__in=followed_users).distinct()
    query = request.GET.get('q', '')
    search_results = None
    if query:
        search_results = Album.objects.filter(title__icontains=query)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('partial') == 'todays_albums':
        return render(request, 'album_rater/_todays_albums.html', {'todays_albums': todays_albums, 'query': query})
    context = {
        'top_rated_albums': top_rated_albums,
        'todays_albums': todays_albums,
        'followed_albums': followed_albums,
        'search_results': search_results,
        'query': query,
    }
    return render(request, 'album_rater/index.html', context)

def about(request):
    return render(request, 'album_rater/about.html')

def account_register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            messages.success(request, "Registration successful! Please log in.")
            return redirect(reverse('album_rater:login'))
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'album_rater/sign_up.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

def account_login(request):
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
            messages.error(request, "Invalid login details supplied.")
            return redirect(reverse('album_rater:login'))
    else:
        return render(request, 'album_rater/log_in.html')

@login_required
def account_logout(request):
    logout(request)
    return redirect(reverse('album_rater:index'))

@login_required
def account_password_change(request):
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
    return render(request, 'album_rater/change_password.html')

@login_required
def account_delete(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not password or not confirm_password:
            messages.error(request, "Please fill in both password fields.")
            return render(request, 'album_rater/delete_account.html')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'album_rater/delete_account.html')
        user = authenticate(username=request.user.username, password=password)
        if user:
            user.delete()
            logout(request)
            messages.success(request, "Account deleted")
            return redirect('album_rater:index')
        else:
            messages.error(request, "Password is incorrect")
    return render(request, 'album_rater/delete_account.html')

@login_required
def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            user_profile = get_object_or_404(UserProfile, user=request.user)
            album.uploader = user_profile
            album.upload_date = timezone.now().date()
            album.save()
            messages.success(request, "Album created successfully!")
            return redirect(reverse('album_rater:album_detail', args=[album.slug]))
    else:
        form = AlbumForm()
    return render(request, 'album_rater/upload.html', {'form': form})

@login_required
def edit_album(request, album_slug):
    album_obj = get_object_or_404(Album, slug=album_slug)
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if album_obj.uploader != current_profile:
        messages.error(request, "You are not authorized to edit this album.")
        return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Album updated successfully!")
            return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AlbumForm(instance=album_obj)
    context = {
        'form': form,
        'album': album_obj,
    }
    return render(request, 'album_rater/edit_album.html', context)

@login_required
def delete_album(request, album_slug):
    album_obj = get_object_or_404(Album, slug=album_slug)
    current_profile = get_object_or_404(UserProfile, user=request.user)
    if album_obj.uploader != current_profile:
        messages.error(request, "You are not authorized to delete this album.")
        return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))
    if request.method == "POST":
        album_obj.delete()
        messages.success(request, "Album deleted successfully.")
        return redirect(reverse('album_rater:index'))
    return render(request, 'album_rater/delete_album.html', {'album': album_obj})

def album(request, album_slug):
    album_obj = get_object_or_404(Album, slug=album_slug)
    current_profile = None
    user_comment = None
    if request.user.is_authenticated:
        current_profile = get_object_or_404(UserProfile, user=request.user)
        user_comment = Comment.objects.filter(album=album_obj, user_profile=current_profile).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"status": "error", "message": "You must be logged in to comment."})
            messages.error(request, "You must be logged in to comment.")
            return redirect(reverse('album_rater:login'))
        if album_obj.uploader == current_profile:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"status": "error", "message": "You cannot comment on your own album."})
            messages.error(request, "You cannot comment on your own album.")
            return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment_text = form.cleaned_data['text']
                rating_value = form.cleaned_data['rating_value']
                if user_comment:
                    user_comment.text = comment_text
                    user_comment.rating_value = rating_value
                    user_comment.save()
                    message = "Comment updated successfully."
                else:
                    user_comment = Comment.objects.create(
                        text=comment_text,
                        user_profile=current_profile,
                        album=album_obj,
                        score=0,
                        rating_value=rating_value
                    )
                    message = "Comment added successfully."
            else:
                error_msg = ""
                for field, errors in form.errors.items():
                    error_msg += f"{field}: {' '.join(errors)} "
                error_msg = error_msg.strip()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({"status": "error", "message": error_msg})
                messages.error(request, error_msg)
                return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            comments_list = Comment.objects.filter(album=album_obj)
            paginator_comments = Paginator(comments_list, 5)
            page_comments = request.GET.get('page_comments') or 1
            try:
                comments_paginated = paginator_comments.page(page_comments)
            except PageNotAnInteger:
                comments_paginated = paginator_comments.page(1)
            except EmptyPage:
                comments_paginated = paginator_comments.page(paginator_comments.num_pages)
            rendered_comments = render_to_string('album_rater/_comments_list.html', {'comments': comments_paginated, 'album': album_obj})
            # Calculate the updated average rating value
            avg_rating = round(comments_list.aggregate(avg=Avg('rating_value'))['avg'] or 0, 1)
            return JsonResponse({
                "status": "success",
                "message": message,
                "comments_html": rendered_comments,
                "comment_text": comment_text,
                "rating_value": rating_value,
                "button_text": "Edit Comment",
                "button_class": "btn btn-primary",
                "average_rating": avg_rating
            })
        return redirect(reverse('album_rater:album_detail', args=[album_obj.slug]))

    comments_list = Comment.objects.filter(album=album_obj)
    paginator_comments = Paginator(comments_list, 5)
    page_comments = request.GET.get('page_comments') or 1
    try:
        comments_paginated = paginator_comments.page(page_comments)
    except PageNotAnInteger:
        comments_paginated = paginator_comments.page(1)
    except EmptyPage:
        comments_paginated = paginator_comments.page(paginator_comments.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('partial') == 'comments':
        return render(request, 'album_rater/_comments_list.html', {'comments': comments_paginated, 'album': album_obj})

    context = {
        'album': album_obj,
        'comments': comments_paginated,
        'average_rating': round(comments_list.aggregate(avg=Avg('rating_value'))['avg'] or 0, 1) if comments_list.exists() else None,
        'comment_form': CommentForm(initial={'text': user_comment.text if user_comment else '',
                                               'rating_value': user_comment.rating_value if user_comment else ''}),
        'user_comment': user_comment,
    }
    response = render(request, 'album_rater/album.html', context)
    if request.user.is_authenticated:
        viewed_albums = request.session.get('viewed_albums', [])
        if album_obj.id not in viewed_albums:
            album_obj.views += 1
            album_obj.save()
            viewed_albums.append(album_obj.id)
            request.session['viewed_albums'] = viewed_albums
    return response

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    uploaded_albums = Album.objects.filter(uploader=user_profile)
    rated_albums = Album.objects.filter(ratings__user_profile=user_profile).exclude(uploader=user_profile).distinct()
    is_following = False
    if request.user.is_authenticated:
        current_profile = get_object_or_404(UserProfile, user=request.user)
        if user_profile in current_profile.users_followed.all():
            is_following = True

    paginator_uploaded = Paginator(uploaded_albums, 6)
    page_uploaded = request.GET.get('page_uploaded')
    try:
        uploaded_albums_paginated = paginator_uploaded.page(page_uploaded)
    except PageNotAnInteger:
        uploaded_albums_paginated = paginator_uploaded.page(1)
    except EmptyPage:
        uploaded_albums_paginated = paginator_uploaded.page(paginator_uploaded.num_pages)

    paginator_rated = Paginator(rated_albums, 6)
    page_rated = request.GET.get('page_rated')
    try:
        rated_albums_paginated = paginator_rated.page(page_rated)
    except PageNotAnInteger:
        rated_albums_paginated = paginator_rated.page(1)
    except EmptyPage:
        rated_albums_paginated = paginator_rated.page(paginator_rated.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        partial = request.GET.get('partial')
        if partial == 'uploaded_albums':
            return render(request, 'album_rater/_uploaded_albums.html', {'uploaded_albums': uploaded_albums_paginated})
        elif partial == 'rated_albums':
            return render(request, 'album_rater/_rated_albums.html', {'rated_albums': rated_albums_paginated})

    context = {
        'user_profile': user_profile,
        'uploaded_albums': uploaded_albums_paginated,
        'rated_albums': rated_albums_paginated,
        'is_following': is_following,
    }
    return render(request, 'album_rater/profile.html', context)

def search(request):
    query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', '')
    genre_filter = request.GET.get('genre', '')
    album_results = Album.objects.all()
    user_results = User.objects.all()

    if query:
        album_results = album_results.filter(title__icontains=query)
        user_results = user_results.filter(username__icontains=query)

    if genre_filter:
        album_results = album_results.filter(genre=genre_filter)

    if sort_option == 'top':
        album_results = album_results.order_by('-views')
    elif sort_option == 'new':
        album_results = album_results.order_by('-upload_date')

    paginator_albums = Paginator(album_results, 18)
    page_albums = request.GET.get('page_albums')
    try:
        album_results_paginated = paginator_albums.page(page_albums)
    except PageNotAnInteger:
        album_results_paginated = paginator_albums.page(1)
    except EmptyPage:
        album_results_paginated = paginator_albums.page(paginator_albums.num_pages)

    paginator_users = Paginator(user_results, 18)
    page_users = request.GET.get('page_users')
    try:
        user_results_paginated = paginator_users.page(page_users)
    except PageNotAnInteger:
        user_results_paginated = paginator_users.page(1)
    except EmptyPage:
        user_results_paginated = paginator_users.page(paginator_users.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        partial = request.GET.get('partial')
        if partial == 'albums_search':
            return render(request, 'album_rater/_albums_search.html', {'albums': album_results_paginated, 'query': query, 'sort': sort_option, 'genre': genre_filter})
        elif partial == 'users_search':
            return render(request, 'album_rater/_users_search.html', {'users': user_results_paginated, 'query': query, 'sort': sort_option, 'genre': genre_filter})

    context = {
        'albums': album_results_paginated,
        'users': user_results_paginated,
        'query': query,
        'sort': sort_option,
        'genre': genre_filter,
    }
    return render(request, 'album_rater/search.html', context)

@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect(reverse('album_rater:user_profile', kwargs={'username': request.user.username}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=user_profile)
    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'album_rater/edit_profile.html', context)
