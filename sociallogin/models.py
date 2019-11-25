from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Document(models.Model):
    """
    created a model for uploading a document
    """
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()

    def __str__(self):
        return self.upload.name


class Posts(models.Model):
    """
    created a model for uploading a document
    """
    title = models.CharField(max_length=10)
    content = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class File(models.Model):
    """
    created a model for uploading a file
    """
    file = models.ImageField(blank=False, null=False)

    def __str__(self):
        return self.file.name


