
from django.db import models

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class Profile(models.Model):

    firstName = models.CharField(max_length=255, verbose_name='firstName')
    lastName = models.CharField(max_length=255, verbose_name='lastName')
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    address = models.CharField(blank=True, null=True, max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
