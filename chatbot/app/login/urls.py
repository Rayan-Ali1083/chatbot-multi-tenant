from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import login_view, main_view, upload_data
 


urlpatterns = [
    path('', login_view, name='login'),
    path('main/', main_view, name='main'),
    path('upload_data/', upload_data, name='upload_data'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
]