"""
Description:
This describes the rest API views using the django rest framework ,when
requests are passed to the handler methods (get,post)which are REST framework's Request instances
Handler methods return REST framework's Response
Author: pooja adhikari
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from fundoonote.settings import BASE_DIR, AWS_STORAGE_BUCKET_NAME
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from services.aws import delete_file, upload_file
from services.utils import smd_response
from .serializers import FileSerializer, DocumentSerializer, PostsShareSerializer
import os


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


class S3FileUploadView(GenericAPIView):
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
            upload_file(os.path.join(BASE_DIR, 'templates') + '/' + request.FILES['file'].name,
                        AWS_STORAGE_BUCKET_NAME)
            smd = Response({
                "success": True,
                "message": 'The file is successfully uploaded to Aws S3 bucket'})

        else:
            smd = Response({
                "success": False,
                "message": 'The file is not uploaded successfully '})
        return smd


class S3FileDeleteView(GenericAPIView):
    serializer_class = FileSerializer

    def delete(self, request, file_name):
        # file_name = request.FILES['file'].name
        delete_file(file_name)
        smd = Response({
            "success": True,
            "message": 'The file is deleted from the S3 bucket'})
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
