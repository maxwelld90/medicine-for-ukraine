from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    flag_url = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.name

class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address_lines = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f'{self.country.name} Address'