"""
Description:
The urls file allows the user to access the REST API views using the urls set by the user
THE DJANGO engine first looks up the urls.py file to refer to the urls for the API views as implemented in the views.py
file
Author: Pooja Adhikari
"""
from django.urls import path
from sociallogin.views import DocumentUploadView, PostsShareView,S3FileUploadView,S3FileDeleteView

urlpatterns = [
    path('document/', DocumentUploadView.as_view(), name='media'),
    path('post/', PostsShareView.as_view(), name='posts'),
    path('S3fileupload/', S3FileUploadView.as_view(), name='awsfileupload'),
    path('S3filedelete/<file_name>/', S3FileDeleteView.as_view(), name='awsfiledelete')
]
