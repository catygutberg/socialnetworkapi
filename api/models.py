from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    like = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)


class UserInfo(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, primary_key=True, on_delete=models.PROTECT)
    last_request = models.DateTimeField()

