from django.db import models

class GenderChoices(models.TextChoices):
    M = ('M', 'Men')
    W = ('W', 'Women')
    U = ('U', 'Unisex')
    K = ('K', 'Kids')

