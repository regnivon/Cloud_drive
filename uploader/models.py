from django.db import models


# Create your models here.

class StoredObject(models.Model):
    name = models.CharField(max_length=200)
    submit_date = models.DateTimeField("Upload Date")
    owner = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.submit_date} {self.owner}"
