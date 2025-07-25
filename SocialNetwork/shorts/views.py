from django.shortcuts import render, redirect
from .forms import ShortForm
from .models import Short, ShortComment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Short, ShortLike
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import ShortCommentForm

# Upload a new short video
@login_required
def upload_short(request):
    if request.method == 'POST':
        form = ShortForm(request.POST, request.FILES)
        if form.is_valid():
            short = form.save(commit=False)
            short.user = request.user
            short.save()
            return redirect('shorts_feed')  # ✅ redirect after successful upload
    else:
        form = ShortForm()
    
    return render(request, 'shorts/upload.html', {'form': form})  # ✅ render upload form if GET request

# View to show all shorts and handle commenting via POST
def shorts_feed(request):
    shorts = Short.objects.prefetch_related('comments').order_by('-created_at')  # Load all shorts with comments

    if request.method == 'POST':
        short_id = request.POST.get('short_id')
        short = get_object_or_404(Short, id=short_id)
        form = ShortCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.short = short
            comment.user = request.user
            comment.save()
            return redirect('shorts_feed')
    else:
        form = ShortCommentForm()
        
    return render(request, 'shorts/feed.html', {'shorts': shorts, 'form': form})

# Like or unlike a short
@login_required
def like_short(request, short_id):
    if request.method == "POST":
        short = get_object_or_404(Short, id=short_id)
        like_obj, created = ShortLike.objects.get_or_create(user=request.user, short=short)

        if not created:
            like_obj.delete()  # Unlike
            liked = False
        else:
            liked = True  # Liked

        return JsonResponse({
            'liked': liked,
            'total_likes': short.total_likes()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Add a comment to a short via AJAX
@require_POST
@login_required
def add_short_comment(request, short_id):
    short = get_object_or_404(Short, id=short_id)
    text = request.POST.get("text")
    if text:
        comment = ShortComment.objects.create(short=short, user=request.user, text=text)
        html = render_to_string("shorts/partials/comment.html", {"comment": comment})  # Render comment partial
        return JsonResponse({"success": True, "comment_html": html})
    return JsonResponse({"success": False, "error": "Text is empty."})
