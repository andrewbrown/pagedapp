from django.db import models


class Subscriber(models.Model):
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=254)


class Message(models.Model):
    received_date = models.DateTimeField(default=None)
    sender = models.CharField(max_length=32, default=None)
    message = models.CharField(max_length=1600, default=None)
    post_serialized = models.TextField()
    sent = models.BooleanField(default=False)
    debug = models.BooleanField(default=False)
