from django.db import models

# Create your models here.

class Members(models.Model):
  id = models.IntegerField(primary_key=True)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  flag = models.CharField(max_length=255)