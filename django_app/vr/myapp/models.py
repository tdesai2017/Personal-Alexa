from django.db import models
from datetime import datetime

# Create your models here.

class ShoppingListItem(models.Model):
    name = models.CharField(max_length=250)

class Reminder(models.Model):
    text = models.TextField()