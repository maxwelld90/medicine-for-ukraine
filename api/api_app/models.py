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

class ItemPrice(models.Model):
    url = models.URLField(primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    last_checked = models.DateTimeField()

    def __str__(self):
        return f'{self.url}'