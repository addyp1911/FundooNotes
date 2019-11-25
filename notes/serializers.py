"""
******************************************************************************
* Purpose: purpose is to define the serializers which are very similar to a Django Form class, and
includes similar validation flags on the various fields, such as required, max_length and default.
Serializers allow complex data such as querysets and model instances to be converted to native Python
datatypes that can then be easily rendered into JSON, XML or other content types
.
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from .documents import NoteDocument
from .models import Label, Note, EmailTemplate


class LabelSerializer(serializers.ModelSerializer):
    """
    A serializer defined for the model Label
    """

    class Meta:
        model = Label
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    """
    A serializer defined for the model Note
    """

    class Meta:
        model = Note
        fields = '__all__'


class EmailTemplateSerializer(serializers.ModelSerializer):
    """
    A serializer defined for the model Email Template
    """

    class Meta:
        model = EmailTemplate
        fields = '__all__'


class NoteDocumentSerializer(DocumentSerializer):
    """Serializer for the document."""

    label = serializers.SerializerMethodField()
    collaborator = serializers.SerializerMethodField()

    class Meta(object):
        """Meta options."""

        document = NoteDocument

        fields = (
            'id',
            'title',
            'content',
            'label',
            'collaborator',
            'reminder',
        )

    def get_label(self, obj):
        return {'labels': x.label for x in obj.label.all()}

    def get_collaborator(self, obj):
        return {'collaborators': x.username for x in obj.collaborator.all()}
