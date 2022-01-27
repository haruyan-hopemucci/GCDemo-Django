from django.db import models

# Create your models here.
class Area(models.Model):
  name = models.CharField(max_length=80)

  def __str__(self) -> str:
    return f'pk={self.pk}, name={self.name}'

class GcType(models.Model):
  name = models.CharField(max_length=80)
  imagebase64 = models.TextField()

  def __str__(self) -> str:
    return f'pk={self.pk}, name={self.name}'

class GcDay(models.Model):
  area = models.ForeignKey(Area, on_delete=models.CASCADE)
  gcdate = models.DateField()
  gctype = models.ForeignKey(GcType, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return f'pk={self.pk}, gcdate={self.gcdate}, gctype={self.gctype}'
  