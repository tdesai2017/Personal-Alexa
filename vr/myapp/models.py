from django.db import models
from datetime import datetime

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=250)
