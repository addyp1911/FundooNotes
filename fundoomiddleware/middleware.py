import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from notes.models import Label, Note


class CheckLabelMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        try:
            if request.path.startswith('/api/labels/'):
                label_id = view_args[1]['label_id']
                label = Label.objects.get(id=label_id)
                if label is not None:
                    print("The label id is valid")
            elif request.path.startswith('/api/notes/'):
                note_id = view_args[1]['note_id']
                note = Note.objects.get(id=note_id)
                if note is not None:
                    print("The note id is valid")
            elif request.path.startswith('/api/note/') and request.method == 'POST':
                body = json.loads(request.body)
                for collab in body['collaborator']:
                    if collab not in [user.email for user in User.objects.all()] and collab == request.user.email:
                        return JsonResponse({'exception': "The collaborator is invalid"})
                for label in body['label']:
                    if label not in [lab.label for lab in Label.objects.all()]:
                        return JsonResponse({'exception': "The label is invalid"})
        except (Label.DoesNotExist, Note.DoesNotExist):
            exception = None
            response = self.process_exception(request, exception)
            return response

    def process_exception(self, request, exception):
        return JsonResponse({'exception': exception.__class__.__name__})
