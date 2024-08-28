from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.name