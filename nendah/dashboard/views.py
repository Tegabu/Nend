from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from socialspace.models import Listing

# Create your views here.


@login_required
def index(request):
    listing = Listing.objects.filter(host_name=request.user)

    return render(request, 'dashboard/index.html', {'listing': listing})
