from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth


# Create your views here.


def register(request):
    if request.method == 'POST':
        user = request.POST['username']
        email = request.POST['email']
        password = request.POST['pword']
        password2 = request.POST['re_pword']

        user = User.objects.creat_user(
            user=user, password=password, email=email)
        user.save()
        print("user created")
        return redirect('/')

    else:
        return render(request, 'socialspace/signup.html')
