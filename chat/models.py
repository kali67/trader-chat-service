from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    users = models.ManyToManyField(User)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    sent_timestamp = models.DateTimeField()
    received_timestamp = models.DateTimeField(null=True)
