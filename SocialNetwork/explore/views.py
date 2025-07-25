from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# View for global search across users and posts
@login_required
def global_search(request):
    query = request.GET.get('q')  # Get the search query from the URL parameters
    user_results = []
    post_results = []

    if query:
        query_clean = query.lstrip('#')  # Remove leading '#' if present
        user_results = User.objects.filter(username__icontains=query_clean)  # Search users by username
        content_results = Post.objects.filter(content__icontains=query_clean)  # Search posts by content
        tag_results = Post.objects.filter(tags__name__icontains=query_clean)  # Search posts by tag names
        post_results = (content_results | tag_results).distinct()  # Combine and remove duplicates

    # Render the search results in the global_search template
    return render(request, 'explore/global_search.html', {
        'query': query,
        'user_results': user_results,
        'post_results': post_results,
    })

# AJAX endpoint for search suggestions
@require_GET
@login_required
def ajax_search_suggestions(request):
    query = request.GET.get('q','').lstrip('#')  # Get query and remove leading '#'
    user_suggestions = []
    post_suggestions = []

    if query:
        # Get up to 5 usernames matching the query
        user_suggestions = list(User.objects.filter(username__icontains=query)
                                .values_list('username', flat=True)[:5])
        # Get up to 5 post snippets (content and username) matching the query
        post_suggestions = list(Post.objects.filter(content__icontains=query)
                                .values('content', 'user__username', 'id')[:5])

    # Return the suggestions as JSON
    return JsonResponse({
        'users': user_suggestions,
        'posts': post_suggestions,
    })
