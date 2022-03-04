from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=256, unique=True)
    flag_url = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.name