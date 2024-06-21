from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import *
 


urlpatterns = [
    path('', login_view, name='login'),
    path('main/', main_view, name='main'),
    path('upload_data/', upload_data, name='upload_data'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    # API views
    path('create_collection/', create_collection, name='create_collection'),
    path('add_docs/', add_docs, name='add_docs'),
    path('add_doc/', add_doc, name='add_doc'),
    path('search_docs/', search_docs, name='search_docs'),
    path('edit_doc/', edit_doc, name='edit_doc'),
    path('delete_docs/', delete_docs, name='delete_docs'),
    path('predict/', predict, name='predict'),

]