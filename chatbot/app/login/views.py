from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .utilities import get_tenant

# Create your views here.
def login_view(request):
    tenant = get_tenant(request)
    print(f'Tenant: {tenant}')
    print('Login view executed')  # Debug statement
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('main')
        else:
            # Invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html', {'tenant': tenant})

    
@login_required
def main_view(request):
    tenant = get_tenant(request)
    return render(request, 'main.html', {'tenant': tenant})

@login_required
def upload_data(request):
    return render(request, 'upload_data.html')

