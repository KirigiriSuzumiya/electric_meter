from django.db import models

# Create your models here.
class Info(models.Model):
    number = models.DecimalField(decimal_places=4, max_digits=100, blank=True, null=True)
    info = models.TextField(max_length=1000,blank=True, null=True)
    image = models.CharField(max_length=1000)
    upload_time = models.DateTimeField()

    def __str__(self):
        return self.image
