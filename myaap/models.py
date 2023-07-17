from django.db import models
from autoslug import AutoSlugField

class Post(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None) 
    