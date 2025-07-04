from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class ExpenseIncome(models.Model):


    class TransactionType(models.TextChoices):
        CREDIT = 'credit', 'Credit'
        DEBIT = 'debit', 'Debit'

    class TaxType(models.TextChoices):
        FLAT = 'flat', 'Flat'
        PERCENTAGE = 'percentage', 'Percentage'

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null= True)
    amount = models.DecimalField(max_digits=10, decimal_places= 2)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_type = models.CharField(max_length=10, choices=TaxType.choices, default=TaxType.FLAT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def total_amount(self):
        if self.tax_type == self.TaxType.FLAT:
            return self.amount + self.tax
        elif self.tax_type == self.TaxType.PERCENTAGE:
            return self.amount + (self.amount * self.tax/Decimal('100'))
        

    def __str__(self):
        return self.title

