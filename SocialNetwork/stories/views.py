from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Story
from .forms import StoryForm
from django.contrib.auth.models import User

# View for uploading a story (image or video)
@login_required
def story_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        # User cannot upload both an image and a video at the same time
        if image and video:
            return render(request, 'stories/story_upload.html', {
                'error': 'Upload either an image or a video, not both at the same time.'
            })

        # User must upload at least one file
        if not image and not video:
            return render(request, 'stories/story_upload.html', {
                'error': 'You must upload at least an image or a video.'
            })

        # Create and save the story
        Story.objects.create(user=request.user, image=image, video=video)
        return redirect('home')

    # Render the upload page for GET requests
    return render(request, 'stories/story_upload.html')


# View to display a specific story for a given user
@login_required
def view_story(request, username, index=0):
    user = get_object_or_404(User, username=username)
    stories = Story.objects.filter(user=user).order_by('created_at')  # Get all stories by the user
    current_story = stories[int(index)]  # Get the specific story by index
    return render(request, 'stories/view_story.html', {'story': current_story, 'story_user': user})
