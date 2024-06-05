from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utilities import get_tenant
from .models import Member

# Create your views here.
def login_view(request):
    tenant = get_tenant(request)
    
    if request.method == 'POST':
        print('POST request received')  
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(tenant)
        user = authenticate(request, username=username, password=password)    
        if user is not None:
            print('User authenticated successfully') 
            login(request, user)
            return redirect('main')
        else:
            print('Invalid username or password')  
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    else:
        print('GET request received')  
        return render(request, 'registration/login.html', {'tenant': tenant})


    
@login_required
def main_view(request):
    tenant = get_tenant(request)
    return render(request, 'main.html', {'tenant': tenant})

@login_required
def upload_data(request):
    tenant = get_tenant(request)
    print(tenant)
    print('open upload')
    return render(request, 'upload_data.html')

