from django.db import models


class Pokemon(models.Model):
    national_number = models.SmallIntegerField()
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    species = models.CharField(max_length=200, default='DEFAULT VALUE')
    height_meters = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    height_imperial = models.CharField(max_length=200, default='DEFAULT VALUE')
    weight_grams = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    weight_imperial = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    abilities = models.CharField(max_length=200, default='DEFAULT VALUE')

    def __str__(self):
        return f"{self.national_number} {self.name} Type: {self.type}\n"
