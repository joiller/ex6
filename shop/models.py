from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.


class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,null=False)
    password = models.CharField(max_length=100,null=False)
    balance = models.FloatField()

    def __str__(self):
        return self.name


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,null=False)
    price = models.FloatField()
    volume = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transaction(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    account = models.ForeignKey('Account', related_name='transactions', on_delete=models.CASCADE)

    class Statuses(models.IntegerChoices):
        COMPLETED = 0
        REFUNDED = 1
        EXPIRED = 2
        CANCELED = 3
    status = models.IntegerField(choices=Statuses.choices,default=0)


class Charge(Transaction):
    from_card = models.CharField(max_length=100)


class Purchase(Transaction):
    volume = models.PositiveIntegerField()
    product = models.ForeignKey(Product,models.CASCADE, related_name='purchase')


class Extraction(Transaction):
    to_card = models.CharField(max_length=100)
