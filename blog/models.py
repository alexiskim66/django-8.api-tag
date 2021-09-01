from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings 
from django.urls import reverse
from taggit.managers import TaggableManager
from django.views.generic import ListView, DetailView,TemplateView


class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to = "blog/", blank=True, null=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:200]


class Comment(models.Model):
    post_id = models.ForeignKey("Blog", on_delete=models.CASCADE, db_column="post_id")
    comment_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    body = models.TextField()
