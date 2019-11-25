"""
Description:
This describes the rest API views using the django rest framework ,when
requests are passed to the handler methods (get,post)which are REST framework's Request instances
Handler methods return REST framework's Response
Author: pooja adhikari
"""
from django.views.generic import TemplateView
from requests import Response
from rest_framework.generics import GenericAPIView
from django.shortcuts import render
from rest_framework import status
from .serializers import FileSerializer, DocumentSerializer, PostsShareSerializer
from services.utils import smd_response


class Home(TemplateView):
    """
    an endpoint for showing the home view to the user
    """
    template_name = 'home.html'


class DocumentUploadView(GenericAPIView):
    """
    an end point for uploading a document file
    """
    serializer_class = DocumentSerializer

    def post(self, request, *args, **kwargs):
        """

        :param request:post request for creating a document object in the database
        :return: returns smd response in  accordance with the document upload status
        """

        document_serializer = DocumentSerializer(data=request.data)
        if document_serializer.is_valid():
            document_serializer.save()
            smd = smd_response(
                success=True,
                message='The document is successfully created',
                data=document_serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            smd = smd_response(
                success=False,
                message='The document is not created',
                data=document_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return smd


class FileUploadView(GenericAPIView):
    """
    an endpoint for uploading a media file
    """
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        """

        :param request: post request for creating a file object in the database
        :return: returns smd response in  accordance with the file upload status
        """

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            smd = smd_response(
                success=True,
                message='The file is successfully created',
                data=file_serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            smd = smd_response(
                success=False,
                message='The file is not created',
                data=file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return smd


class PostsShareView(GenericAPIView):
    """
    an endpoint for sharing the note on any social application as given by the user
    """
    serializer_class = PostsShareSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request:  post request for creating a note object in the database
        :return: renders the serializer data on any social application ,or returns smd response in case of bad request
        """
        post_serializer = PostsShareSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            note_data = post_serializer.validated_data
            title = note_data['title']
            content = note_data['content']
            # return redirect
            # ('https://twitter.com/intent/tweet?url=https://twitter.com/poojaad14530254&text='+title+' '+content)
            return render(request, 'home.html', {'title': title, 'content': content}, status=status.HTTP_201_CREATED)
        else:
            smd = smd_response(
                success=False,
                message='The note is not created/shared',
                data=post_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return smd




