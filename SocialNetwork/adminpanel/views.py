from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from users.models import Profile
from django.contrib.auth.decorators import user_passes_test

# Check if the user is an admin (superuser)
def is_admin(user):
    return user.is_superuser

# Admin dashboard view - only accessible to admin users
@user_passes_test(is_admin)
def admin_dashboard(request):
    posts = Post.objects.all()  # Retrieve all posts
    user = Profile.objects.all()  # Retrieve all user profiles
    return render(request, 'adminpanel/dashboard.html', {
        'posts': posts,
        'profile' : Profile,  # Pass the Profile model to the template
    })

# View to delete a post by ID - only accessible to admin users
@user_passes_test(is_admin)    
def delete_post(request, post_id):  
    post = get_object_or_404(Post, id=post_id)  # Get the post or return 404
    post.delete()  # Delete the post
    return redirect('admin_dashboard')  # Redirect back to admin dashboard

# View to delete a user (Profile) by ID
def delete_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)  # Get the user profile or return 404
    user.delete()  # Delete the user profile
    return redirect('admin_dashboard')  # Redirect back to admin dashboard
