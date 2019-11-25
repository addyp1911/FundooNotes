"""
Description:
The urls file allows the user to access the REST API views using the urls set by the user
THE DJANGO engine first looks up the urls.py file to refer to the urls for the API views as implemented in the views.py
file
Author: Pooja Adhikari
"""
from django.urls import path
from sociallogin.views import FileUploadView, DocumentUploadView, PostsShareView

urlpatterns = [
    path('file/', FileUploadView.as_view(), name='file-upload'),
    path('document/', DocumentUploadView.as_view(), name='media'),
    path('post/', PostsShareView.as_view(), name='posts'),
]
