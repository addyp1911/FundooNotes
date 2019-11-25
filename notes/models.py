"""
******************************************************************************
* Purpose: purpose is to define the models Note and Label for this app
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import json

from django.contrib.auth.models import User
from django.db import models


class Label(models.Model):
    """
    created a model for Labels,also used for a many to many relationship with the Note model
    """
    label = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('label', 'user',)

    def __str__(self):
        return self.label


class Note(models.Model):
    """
     created a model for Notes, where User model is used as a foreign key and a many to many relationship is maintained
     with both Label model and User model
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    time_stamp = models.DateTimeField(auto_now_add=True)
    label = models.ManyToManyField(Label, related_name='notelabel', blank=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator', blank=True)
    is_archive = models.BooleanField(default=False)
    is_pin = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    image = models.FileField(blank=True, null=True)
    reminder = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def label_indexing(self):
        """labels for indexing.

        Used in Elastic search indexing.
        """
        return json.dumps([note_label.label for note_label in self.label.all()])

    @property
    def collaborator_indexing(self):
        """collaborator for indexing.

        Used in Elastic search indexing.
        """
        return json.dumps([note_collaborator.username for note_collaborator in self.collaborator.all()])

    @property
    def user_indexing(self):
        """user for indexing.

        Used in Elastic search indexing.
        """
        if self.user is not None:
            return self.user.id


class EmailTemplate(models.Model):
    """
    Email templates get stored in database so that admins can
    change emails on the fly
    """
    subject = models.CharField(max_length=255, blank=True, null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255, blank=True, null=True)
    plain_text = models.TextField(blank=True, null=True)
    is_html = models.BooleanField(default=False)
    is_text = models.BooleanField(default=False)
    template_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "<{}> {}".format(self.template_key, self.subject)
