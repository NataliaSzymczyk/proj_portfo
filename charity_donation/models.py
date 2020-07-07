from django.db import models
from django.contrib.auth.models import User


TYPES = [
    ('Fundacja', 'Fundacja'),
    ('Organizacja_pozarządowa', 'Organizacja pozarządowa'),
    ('Zbiórka_lokalna', 'Zbiórka lokalna'),
]


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    name = models. CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=64, choices=TYPES, default='Fundacja')
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity =  models.IntegerField(verbose_name='Liczba worków')
    categories = models.ManyToManyField(Category)
    institution =models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)


