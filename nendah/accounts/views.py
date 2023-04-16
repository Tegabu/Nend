from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth


# Create your views here.


def register(request):
    if request.method == 'POST':
        user = request.POST.get['username']
        email = request.POST.get['email']
        password = request.POST.get['pword']
        password2 = request.POST.get['re_pword']

        user = User.objects.creat_user(
            user=user, password=password, email=email)
        user.save()
        print("user created")
        return redirect('/')

    else:
        return render(request, 'landing/signup.html')
