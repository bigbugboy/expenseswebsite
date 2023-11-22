from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now, blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.category
        
    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name
