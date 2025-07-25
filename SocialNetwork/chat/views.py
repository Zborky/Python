from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm

# Display chat between the logged-in user and another user by username
@login_required
def chat_view(request, username):
    # Load the target user or show 404 if not found
    other_user = get_object_or_404(User, username=username)

    # Get all messages between the logged-in user and the target user
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |  # messages sent by the user
        Q(sender=other_user, receiver=request.user)    # messages received by the user
    ).order_by('timestamp')  # ordered by timestamp

    # Simple message sending without using Django Form class
    if request.method == "POST":
        content = request.POST.get("content")  # message text
        image = request.FILES.get("image")     # optional image
        if content or image:
            # Create a new message
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content,
                image=image
            )
            # After sending, redirect back to the chat
            return redirect('chat', username=other_user.username)

    # Render chat template
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_user': other_user,
        'user': request.user,  
    })


@login_required
def private_chat(request, username):
    # Load the target user
    other_user = get_object_or_404(User, username=username)

    # Load all messages between the users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        # Use Django form for messages (file + text)
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('private-chat', username=other_user.username)
    else:
        # If GET request, create empty form
        form = MessageForm()

    # Render chat template with form
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'form': form,
        'other_user': other_user,
    })


# Inbox – display list of conversations with last messages
@login_required
def inbox_view(request):
    # Load all messages where the user is either sender or receiver
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')  # newest messages first

    conversations = {}
    for msg in messages:
        # Determine the other user in the conversation
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        # If we haven't added a conversation with this user yet, add the latest message
        if other_user not in conversations:
            conversations[other_user] = msg

    # Render inbox template with list of last messages per conversation
    return render(request, 'chat/inbox.html', {
        'conversations': conversations
    })
