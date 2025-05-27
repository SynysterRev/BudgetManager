from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="categories")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "Categories"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="transactions")
    datetime = models.DateField()
    description = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0)])
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
