from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views 

urlpatterns = [
    path('', views.login_view, name='login'),
    path('main/', views.main_view, name='main'),
    path('upload_data/', views.upload_data, name='upload_data'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
]
