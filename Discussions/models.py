from django.db import models
from Accounts.models import User
# Create your models here.



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name  

class Discussion(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='Files', max_length=100,  blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-update', '-created')

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    created =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-update', '-created')

    def __str__(self):
        return self.body[0:50]