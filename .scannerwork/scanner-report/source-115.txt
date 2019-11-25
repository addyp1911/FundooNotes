"""
Description:
This describes the serializers which are very similar to a Django Form class, and
includes similar validation flags on the various fields, such as required, max_length and default.
Serializers allow complex data such as querysets and model instances to be converted to native Python
datatypes that can then be easily rendered into JSON, XML or other content types.

Author: Pooja Adhikari
"""
from rest_framework import serializers
from .models import File, Document, Posts


class FileSerializer(serializers.ModelSerializer):
    """
    serializer for the file model
    """

    class Meta:
        model = File
        fields = ['file', ]


class DocumentSerializer(serializers.ModelSerializer):
    """
    serializer for the document model
    """

    class Meta:
        model = Document
        fields = ['uploaded_at', 'upload']


class PostsShareSerializer(serializers.ModelSerializer):
    """
    serializer for the posts model
    """

    class Meta:
        model = Posts
        fields = ['title', 'content']


