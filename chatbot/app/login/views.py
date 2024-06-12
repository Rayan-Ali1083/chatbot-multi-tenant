from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utilities import get_tenant, all_tenants, get_collection_name
from .models import Member

# Create your views here.
def login_view(request):
    ten = all_tenants(request)
    tenant = get_tenant(request)
    if not tenant:
        return render(request, 'registration/login.html', {'error': 'Invalid tenant'})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Get all members of the current tenant
        members = Member.objects.filter(tenant=tenant)
        if any(member.name == username for member in members):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid password', 'tenant': tenant})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username', 'tenant': tenant})
    else:
        return render(request, 'registration/login.html', {'tenant': tenant, 'all_tenants': ten})



    
@login_required
def main_view(request):
    tenant = get_tenant(request)
    return render(request, 'main.html', {'tenant': tenant})

@login_required
def upload_data(request):
    collection_name = get_collection_name(request)
    return render(request, 'upload_data.html', {'collection_name': collection_name})

