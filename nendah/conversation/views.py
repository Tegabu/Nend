from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from socialspace.models import Listing, Profile, User

from .models import Conversation
from .forms import ConversationMessageForm
# Create your views here.


@login_required
def new_conversation(request, listing_pk):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    item = get_object_or_404(Listing, pk=listing_pk)

    if item.host_name == request.user:
        return redirect('social:dashboard')

    conversations = Conversation.objects.filter(
        item=item).filter(members__in=[request.user.id])

    if conversations:
        pass

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.host_name)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('social:detail', pk=listing_pk)

    else:
        form = ConversationMessageForm()
    return render(request, 'conversation/new.html', {'form': form, 'user_profile': user_profile,  'user_objects': user_objects})


@login_required
def inbox(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {'conversations': conversations, 'user_profile': user_profile,  'user_objects': user_objects})


@login_required
def chat(request, pk):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    conversation = Conversation.objects.filter(
        members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:chat', pk=pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/chat.html', {'conversation': conversation, 'form': form, 'user_profile': user_profile,  'user_objects': user_objects})
