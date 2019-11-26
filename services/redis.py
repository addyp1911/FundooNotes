"""
******************************************************************************
* Purpose: purpose is to define the redis connection and sets the key-value pair in the redis database
for the redis caching of notes so the database is not hit each time notes have to be retrieved,
the cached notes are accessed instead
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import ast
import pdb

import redis
from django.utils import timezone
from notes.models import Note
from notes.serializers import NoteSerializer

redis_obj = redis.StrictRedis(host='localhost', port=6379, db=0)


class RedisConnection:

    def redis_conn_note(self, user_id, serializer):
        new_list = []
        if redis_obj.get(user_id) is None:
            for data in serializer.data:
                new_list.append(dict(data))
            redis_obj.set(user_id, str(new_list))
            data = serializer.data
        else:
            data = redis_obj.get(user_id)
        return data

    def redis_conn_trash(self, note_query_set):
        new_list = []
        for note in note_query_set:
            note_id = 'note' + str(note.id)
            redis_data = redis_obj.get(note_id)
            if redis_data is not None:
                data = redis_data.decode('utf-8')
                redis_dict = ast.literal_eval(data)
            else:
                note_object = Note.objects.filter(id=note.id)
                note_serializer = NoteSerializer(note_object, many=True)
                data = [{k: v for k, v in data.items()} for data in note_serializer.data]
                redis_obj.set(note_id, str(data))
                redis_dict = note_serializer.data
            new_list.append(redis_dict)
        return new_list

    def redis_conn_archive(self, note_query_set):

        new_list = []
        for note in note_query_set:
            note_id = 'note' + str(note.id)
            redis_data = redis_obj.get(note_id)
            if redis_data is not None:
                data = redis_data.decode('utf-8')
                redis_dict = ast.literal_eval(data)
            else:
                note_object = Note.objects.filter(id=note.id)
                note_serializer = NoteSerializer(note_object, many=True)
                data = [{k: v for k, v in data.items()} for data in note_serializer.data]
                redis_obj.set(note_id, str(data))
                redis_dict = note_serializer.data
            new_list.append(redis_dict)
        return new_list

    def redis_conn_reminder(self, reminder_data, reminder_list):
        display_list = []
        fired_list = []
        upcoming_list = []
        count = 0
        current_time = timezone.now()
        for data in reminder_data:
            note_id = 'reminder' + str(data['id'])
            redis_data = redis_obj.get(note_id)
            if redis_data is not None:
                data = redis_data.decode('utf-8')
                display_list.append(ast.literal_eval(data))
            else:
                redis_obj.set(note_id, str(data))
                reminder_time = reminder_list[count]
                if reminder_time <= current_time:
                    data.update({'reminder_status': 'fired'})
                    fired_list.append(data)
                else:
                    data.update({'reminder_status': 'upcoming'})
                    upcoming_list.append(data)
                count += 1
        display_list.append(fired_list + upcoming_list)
        return display_list
