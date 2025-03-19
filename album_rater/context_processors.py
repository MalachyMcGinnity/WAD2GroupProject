from album_rater.models import UserProfile

def global_context(request):
    user_profile = None
    if (request.user.is_authenticated):
        user_profile = UserProfile.objects.get_or_create(user = request.user)[0]
    return {"user_slug": user_profile.slug}
    