from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User  
from .forms import UserRegisterForm, ProfileForm  
from .models import Profile  


# === AUTHENTICATION ===

# Register a new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # Create profile for the new user
            login(request, user)  # Log in the user automatically
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'users/login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# === PROFILE ===

# View and edit user's own profile
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile
    })


# View another user's public profile
@login_required
def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    followers_count = profile.followers.count()  # Number of followers
    following_count = User.objects.filter(profile__followers=user).count()  # Number of users this user follows
    is_following = profile.followers.filter(id=request.user.id).exists()  # Whether the current user is following them

    return render(request, 'users/public_profile.html', {
        'profile_user': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following
    })


# === FOLLOW / UNFOLLOW ===

# Follow a user
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        profile = user_to_follow.profile
        profile.followers.add(request.user)
    return redirect('public-profile', username=username)


# Unfollow a user
@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    profile = user_to_unfollow.profile
    profile.followers.remove(request.user)
    return redirect('public-profile', username=username)
