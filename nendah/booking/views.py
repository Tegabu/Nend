from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Chat functions

from .models import Chat, profile_pic, Listing
from .forms import ChatMessageForm


@ login_required(login_url='login')
def new_chat(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)

    if listing.host_name == request.user:
        return redirect('social:dashboard')
    chat = Chat.objects.filter(listing=listing).filter(
        members__in=[request.user.id])
    if chat:
        pass
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat = Chat.objects.create(listing=listing)
            chat.members.add(request.user)
            chat.members.add(listing.host_name)
            chat.save()

            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()

            return redirect('social:detail', pk=listing_pk)
    else:
        form = ChatMessageForm()

    return render(request, 'landing/book-chat.html', {'form': form})


@ login_required(login_url='login')
def inbox(request):
    chat = Chat.objects.filter(
        members__in=[request.user.id])

    return render(request, 'landing/chat.html', {'chat': chat})


@ login_required(login_url='login')
def conversation(request, pk):
    chat = Chat.objects.filter(
        members__in=[request.user.id]).get(pk=pk)
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()

            chat.save()

            return redirect('social:conversation', pk=pk)
        else:
            form = ChatMessageForm()
    return render(request, 'landing/conversation.html', {'chat': chat, 'form': form})
