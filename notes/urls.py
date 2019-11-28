"""
******************************************************************************
* Purpose: purpose is to define the urls for the API views
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
from django.urls import path

from .views import LabelCreateView, NoteShareView, NoteCreateView, LabelShareView, GetNoteView, \
    GetTrashedNoteView, GetArchivedNoteView, GetReminderNoteView, paginated_note_view, SendEmailView, NoteSearch

urlpatterns = [
    path('labels/<label_id>', LabelShareView.as_view(), name='labels'),
    path('notes/<note_id>', NoteShareView.as_view(), name='notes'),
    path('label/', LabelCreateView.as_view(), name='label'),
    path('note/', NoteCreateView.as_view(), name='note'),
    path('note/get/', GetNoteView.as_view(), name='note-list'),
    path('notes/trashed/', GetTrashedNoteView.as_view(), name='trash'),
    path('notes/archived/', GetArchivedNoteView.as_view(), name='archived'),
    path('notes/reminders/', GetReminderNoteView.as_view(), name='reminders'),
    # path('bypage/', NotesListView.as_view(), name='notes'),
    path('notesbypage/', paginated_note_view, name='note'),
    path('sendmail/', SendEmailView.as_view(), name='email'),
    path('note/search/<note>', NoteSearch.as_view(), name='search-notes'),


]
