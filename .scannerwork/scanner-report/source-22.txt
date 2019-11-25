from django.contrib import admin
from .models import Label, Note, EmailTemplate

admin.site.register(Note)
admin.site.register(Label)
admin.site.register(EmailTemplate)
