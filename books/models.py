from django.db import models
from django.conf import settings

from core.models import BaseModel

class Book(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=False, blank=True, unique=True)
    description = models.TextField()
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    publisher = models.CharField(max_length=100)
    published_year = models.IntegerField()
    
   
    def __str__(self):
        return self.title