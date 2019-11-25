from datetime import timedelta
from django.utils import timezone


def check_trash(note_query_set):
    for note in enumerate(note_query_set):
        note_obj = note[1]
        time_stamp = note_obj.time_stamp
        now = timezone.now()
        permanent_trash_date = time_stamp + timedelta(days=7)
        if now == permanent_trash_date:
            note_obj.delete()
        return note_obj
