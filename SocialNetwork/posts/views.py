from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from posts.models import Comment, Tag
from .forms import CommentForm
from posts.models import Post
from django.views.decorators.http import require_POST
from django.utils.timezone import localtime

# Like or unlike a post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = request.user in post.likes.all()
    if liked:
        post.likes.remove(request.user)  # Unlike
    else:
        post.likes.add(request.user)  # Like
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'total_likes': post.likes.count()})  # Return updated like count via AJAX
    return redirect('home')

# Add a comment to a post (non-AJAX)
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get("text")
    if text:
        Comment.objects.create(user=request.user, post=post, text=text)
    return redirect("home")

# Add a comment to a post via AJAX
@require_POST
@login_required
def ajax_add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get("text")

    if not text.strip():
        return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)

    comment = Comment.objects.create(user=request.user, post=post, text=text)

    return JsonResponse({
        'username': request.user.username,
        'profile_image_url': request.user.profile.image.url,
        'created_at': localtime(comment.created_at).strftime("%d.%m.%Y %H:%M"),
        'text': comment.text,
        'comment_id': comment.id
    })

# Edit a comment (only by the comment's author)
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'users/edit_comment.html', {'form': form})

# Delete a comment (only by the comment's author)
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'users/delete_comment.html', {'comment': comment})

# Show all posts associated with a specific tag
@login_required
def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name.lower())
    posts = tag.post_set.all().order_by('-created_at')
    return render(request, 'posts/posts_by_tag.html', {'tag': tag, 'posts': posts})

# Display image gallery of a specific user
@login_required
def user_gallery(request, username):
    user = get_object_or_404(User, username=username)
    posts_with_images = Post.objects.filter(user=user, image__isnull=False).exclude(image='')
    return render(request, 'users/gallery.html', {
        'gallery_user': user,
        'posts': posts_with_images
    })
