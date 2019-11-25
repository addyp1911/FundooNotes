"""
******************************************************************************
* Purpose: purpose is to describe the rest API views using the django rest framework ,when
requests are passed to the handler methods (get,post)which are REST framework's Request instances
Handler methods return REST framework's Response
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import pdb

from django.contrib.auth.models import User
from django.core import mail
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from elasticsearch_dsl import Q
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from services.utils import smd_response, logger
from services.redis import RedisConnection, redis_obj
from .documents import NoteDocument
from .models import Label, Note
from .serializers import LabelSerializer, EmailTemplateSerializer, NoteDocumentSerializer
from .serializers import NoteSerializer


class NoteCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request: POST
        :return: returns an SMD response if the note is successfully created or raises a validation error in case of
                 errors with the post data
        :description: post request made to create a new note for a particular user
        """
        try:
            serializer = NoteSerializer(data=request.data, partial=True)
            note_data = request.data
            labels = note_data['label']
            title = note_data['title']
            collaborators = note_data['collaborator']
            current_user = User.objects.get(id=request.user.id)

            label_query_set = Label.objects.filter(label__in=labels, user_id=current_user.id)
            label_list = [label.id for label in label_query_set]

            collaborator_query_set = User.objects.filter(email__in=collaborators)
            collaborator_list = [collaborator.id for collaborator in collaborator_query_set if
                                 collaborator.id != current_user.id]

            serializer.initial_data['label'] = label_list
            serializer.initial_data['collaborator'] = collaborator_list

            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                note_obj = Note.objects.get(id=serializer.data['id'])
                redis_obj.set("note" + str(note_obj.id), str(serializer.data))
                logger.debug("instance created: {})".format(title))
                smd = smd_response(success=True,
                                   message='A new note is created',
                                   data=serializer.data,
                                   status=status.HTTP_201_CREATED)
                logger.info('A new note is created')

            else:
                smd = smd_response(success=False,
                                   message='No note is created',
                                   data=serializer.errors,
                                   status=status.HTTP_400_BAD_REQUEST)
            return smd

        except User.DoesNotExist:
            raise ValidationError("The user matching query does not exist")

        except Label.DoesNotExist:
            raise ValidationError("The label does not exist in the database")

        except KeyError:
            raise ValidationError('Key Error is raised,the fields are not filled correctly')


class NoteShareView(GenericAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, note_id):

        """
        :param note_id: The name parameter is for accessing a note with the note id as given by the user
        :param request: GET
        :return: returns an SMD response accordingly if the note with the name is present/not present in the database
        with the serialized data of the note
        """
        user_id = request.user.id
        data = redis_obj.get('note' + str(note_id))
        if data is None:
            note = Note.objects.filter(id=note_id, user_id=user_id)
            serializer = NoteSerializer(note, many=True)
            note_data = str(serializer.data)
            redis_obj.set('note' + str(note_id), note_data)
            if note.count() == 0:
                raise ValidationError("The note with that id does not exist in the database")
        else:
            note_data = data
        smd = smd_response(
            success=True,
            message='The note is present in database',
            data=note_data,
            status=status.HTTP_200_OK)
        logger.info('Retrieving a note with a particular user entered note id')
        return smd

    def put(self, request, note_id):
        """
        :param request: PUT request
        :param note_id: The name parameter is for accessing a note with the note id as given by the user
        :return: returns an SMD response accordingly if the note with the name is present/not present in the database
                 with the serialized updated data for the note

       """
        try:
            note_obj = Note.objects.get(id=note_id)
            note_data = request.data
            label_query_set = Label.objects.filter(label__in=note_data['label'])
            label_list = []
            collaborator_list = []
            for label in label_query_set:
                label_list.append(label.id)
            note_data['label'] = label_list

            collaborator_query_set = User.objects.filter(email__in=note_data['collaborator'])
            for collaborator in collaborator_query_set:
                collaborator_list.append(collaborator.id)
            note_data['collaborator'] = collaborator_list

            serializer = NoteSerializer(note_obj, data=note_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                redis_obj.set('note' + str(note_obj.id), str(serializer.data))
                logger.debug("Note Object Modified: {})".format(note_obj.title))
                smd = smd_response(
                    success=True,
                    message='The note is recently changed by the user',
                    data=serializer.data,
                    status=status.HTTP_200_OK)

            else:
                smd = smd_response(
                    success=False,
                    message='The note is not changed',
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            return smd

        except User.DoesNotExist:
            raise ValidationError("The user matching query does not exist")

        except Label.DoesNotExist:
            raise ValidationError("The label does not exist in the database")

        except Note.DoesNotExist:
            raise ValidationError("The note with that id does not exist in the database")

    def delete(self, request, note_id):
        """

        :param request: DELETE
        :param note_id: The requested note with respective id is deleted from the database
        :return: returns an SMD response and deleted if the note object exists in the database or else
                 the note is not deleted and response is given accordingly
        """
        try:
            user_id = request.user.id
            data = redis_obj.get('note' + str(note_id))
            if data is not None:
                redis_obj.delete('note' + str(note_id))
                note_obj = Note.objects.get(id=note_id, user_id=user_id, is_trash=False)
                note_obj.delete()
                smd = smd_response(
                    success=True,
                    message='The note is deleted',
                    data='No data',
                    status=status.HTTP_200_OK)
            else:
                smd = smd_response(
                    success=False,
                    message='The note object does not exist in the database',
                    data='No data',
                    status=status.HTTP_204_NO_CONTENT)
            logger.info("Note Delete View Execute")
            return smd

        except Note.DoesNotExist:
            raise ValidationError("The note with that id does not exist in the database")


class GetNoteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def get(self, request):
        """
        :param request: GET
        :return: returns an SMD response when the notes are successfully retrieved else shows a validation error
                 if no note exists for the particular user id
        """
        user_id = request.user.id
        note = Note.objects.filter(user_id=user_id)
        note_serializer = NoteSerializer(note, many=True)
        note_data = RedisConnection.redis_conn_note(self, user_id, note_serializer)
        if len(note_data) > 0:
            smd = smd_response(
                success=True,
                message='The note is present in database',
                data=note_data,
                status=status.HTTP_200_OK)
        else:
            smd = smd_response(
                success=False,
                message='The note does not exist in database',
                data='No data',
                status=status.HTTP_400_BAD_REQUEST)
            logger.info('Retrieving a note with a particular user entered note id')
        return smd


class LabelCreateView(GenericAPIView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        """
        :param request: POST
        :return: returns an SMD response if the label is successfully created or raises a validation error in case of
        errors with the serialized data
        :description: post request made to create a new label for a particular user
        """
        try:
            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid():
                if int(request.data['user']) != User.objects.get(id=request.user.id).id:
                    raise ValidationError("the current user is not valid in this session")
                serializer.save()
                label_obj = Label.objects.get(label=serializer.data['label'])
                redis_obj.set('label' + str(label_obj.id), str(serializer.data))
                logger.debug("Label Object Created: {})".format(label_obj.label))
                smd = smd_response(
                    success=True,
                    message='The respective label is created ',
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                smd = smd_response(
                    success=False,
                    message='The label could not be created ',
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            return smd

        except KeyError:
            raise ValidationError('Key Error is raised,the fields are not filled correctly')


class LabelShareView(GenericAPIView):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, label_id):
        """
        :param request: GET
        :param label_id: The name parameter is for accessing a label with the label id as given by the user
        :return: returns an SMD response accordingly if the label with the name is present/not present in the database
        with the serialized data of the label
        """
        try:
            user_id = request.user.id
            data = redis_obj.get('label' + str(label_id))
            if data is None:
                label_obj = Label.objects.get(id=label_id, user_id=user_id)
                serializer = LabelSerializer(label_obj)
                label_data = serializer.data
            else:
                label_data = data
            smd = smd_response(
                success=True,
                message='label data',
                data=label_data,
                status=status.HTTP_200_OK)
            logger.info('Retrieving a list of notes from the database')
            return smd

        except Label.DoesNotExist:
            return Response('The label with that id and user id does not exist in the database')

    def put(self, request, label_id):
        """
         :param request: PUT request
         :param label_id: The name parameter is for accessing a label with the label idas given by the user
         :return: returns an SMD response accordingly if the note with the name is present/not present in the database
         with the serialized updated data for the note
         """
        try:
            user_id = request.user.id
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data['label']
                label_obj = Label.objects.get(id=label_id, user_id=user_id)
                label_obj.label = title
                label_obj.save()
                redis_obj.set('label' + str(label_id), str(serializer.data))
                logger.debug("Label Object Modified: {})".format(label_obj.label))
                smd = smd_response(
                    success=True,
                    message='label changed',
                    data=serializer.data,
                    status=status.HTTP_200_OK)
            else:
                smd = smd_response(
                    success=False,
                    message='The serializer is not valid',
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            return smd

        except Label.DoesNotExist:
            return Response("The label with that id does not exist in the database")

    def delete(self, request, label_id):
        """
        :param request: DELETE
        :param label_id: The requested label with the particular id is deleted from the database
        :return: returns an SMD response and deleted if the label object exists in the database or else
        the label is not deleted and response is given accordingly
        """
        try:
            user_id = request.user.id
            label_key = 'label' + str(label_id)
            data = redis_obj.get(label_key)
            if data is not None:
                redis_obj.delete(label_key)
                label_obj = Label.objects.filter(id=label_id, user_id=user_id)
                label_obj.delete()
                logger.info('Deleting the label from the database')
                smd = smd_response(
                    success=True,
                    message='The label is deleted',
                    data='No data',
                    status=status.HTTP_200_OK)
            else:
                smd = smd_response(
                    success=False,
                    message='The label does not exist in the database',
                    data='No data',
                    status=status.HTTP_204_NO_CONTENT)

            return smd

        except Label.DoesNotExist:
            raise ValidationError("The label with that id does not exist in the database")


class GetArchivedNoteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def get(self, request):
        """
         :param request: GET
         :return: returns an SMD response when the archived notes are successfully retrieved else shows a validation error
                  if no note exists for the particular user id
         """
        user_id = request.user.id
        note_obj = Note.objects.filter(is_archive=True, user_id=user_id, is_trash=False)
        archive_note_data = RedisConnection.redis_conn_archive(self, note_obj)
        if len(archive_note_data) > 0:
            smd = smd_response(
                success=True,
                message='Archived Notes',
                data=archive_note_data,
                status=status.HTTP_200_OK)
        else:
            smd = smd_response(
                success=False,
                message='Archived Notes do not exist in the database for this user',
                data='No data',
                status=status.HTTP_400_BAD_REQUEST)
        logger.info('Retrieving the archived notes at the particular user id')
        return smd


class GetTrashedNoteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NoteSerializer

    def get(self, request):
        """
         :param request: GET
         :return: returns an SMD response when the trashed notes are successfully retrieved else shows a validation error
                  if no note exists for the particular user id
         """

        note_objects = Note.objects.filter(is_trash=True, user_id=request.user.id)
        trash_note_data = RedisConnection.redis_conn_trash(self, note_objects)
        if len(trash_note_data) > 0:
            smd = smd_response(
                success=True,
                message='Trashed Notes',
                data=trash_note_data,
                status=status.HTTP_200_OK)
        else:
            smd = smd_response(
                success=False,
                message='Trashed notes do not exist in the database',
                data='No data',
                status=status.HTTP_400_BAD_REQUEST)
        logger.info('Retrieving the trashed notes at the particular user id')
        return smd


class GetReminderNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        """

        :param request: GET
        :return: returns a list of reminder notes from the database,displaying the fired notes first followed
                 by upcoming notes
        """

        user_id = request.user.id
        note_objects = Note.objects.filter(user_id=user_id, reminder__isnull=False).order_by("reminder")
        if note_objects.exists():
            serializer = NoteSerializer(note_objects, many=True)
            reminder_data = [{k: v for k, v in data.items()} for data in serializer.data]
            reminders = note_objects.values('reminder')
            reminder_list = []
            for reminder in enumerate(reminders):
                reminder_list.append(reminder[1]['reminder'])
            notes_list = RedisConnection.redis_conn_reminder(self, reminder_data, reminder_list)
            logger.info('Retrieving a list of reminder notes from the database')
            smd = smd_response(success=True,
                               message='reminder notes',
                               data=notes_list,
                               status=status.HTTP_200_OK)
            return smd
        else:
            return Response({'message': 'No reminders exist in the database'})


class SendEmailView(GenericAPIView):
    serializer_class = EmailTemplateSerializer

    def post(self, request, *args, **kwargs):
        """

        :param request: post request for creating a email template object in the database
        :return: returns smd response in  accordance with the file upload status
        """
        email_serializer = EmailTemplateSerializer(data=request.data, partial=True)
        if email_serializer.is_valid():
            email_serializer.save()
            subject = email_serializer.data['subject']
            plain_text = email_serializer.data['plain_text']
            from_email = email_serializer.data['from_email']
            to_email = email_serializer.data['to_email']

            html_content = render_to_string('CustomAlert.html',
                                            {'message': plain_text,
                                             'resetlink': request.get_host() + reverse('forgot-password')})
            msg = mail.EmailMultiAlternatives(subject, plain_text, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info('An email template has been sent to the registered email address')
            smd = smd_response(
                success=True,
                message='The link is successfully sent to the user',
                data=email_serializer.data,
                status=status.HTTP_200_OK)
        else:
            smd = smd_response(
                success=False,
                message='The file is not created',
                data=email_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return smd


def paginated_note_view(request):
    try:
        note_list = Note.objects.all()
        paginator = Paginator(note_list, 3)
        page = request.GET.get('page')
        notes = paginator.get_page(page)
        return render(request, 'notes_list.html', {'notes': notes})
    except (TypeError, ValueError):
        raise PageNotAnInteger('That page number is not an integer')


def search_note(request, note_query):
    if note_query:
        note = NoteDocument.search().query(
            (Q("match", label=note_query) |
             Q("match", content=note_query) |
             Q("match", title=note_query) |
             Q("match", collaborator=note_query)) &
            Q("match", user=request.user.id)
        )

        return note.to_queryset()


class NoteSearch(GenericAPIView):
    serializer_class = NoteDocumentSerializer

    def get(self, request, param):
        searched_notes = search_note(request, param)
        serializer = NoteDocumentSerializer(searched_notes, many=True)
        return Response(serializer.data)
