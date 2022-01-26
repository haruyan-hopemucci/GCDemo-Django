from django.db import models

# Create your models here.
class Area(models.Model):
  name = models.CharField(max_length=80)

class GcType(models.Model):
  name = models.CharField(max_length=80)
  imagebase64 = models.TextField()

class GcDay(models.Model):
  area = models.ForeignKey(Area, on_delete=models.CASCADE)
  gcdate = models.DateField()
  gctype = models.ForeignKey(GcType, on_delete=models.CASCADE)