from django.db import models
from django.db.models import CASCADE


class Customer(models.Model):
    # Manage user types
    USER_TYPE = [
        (1, 'Customer'),
        (2, 'Super User')
    ]
    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    name = models.CharField(max_length=50)
    pin = models.CharField(max_length=5)
    money = models.IntegerField()

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.money, self.pin)



class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.customer.name} of amount {self.amount}"


class ATM(models.Model):
    bills_10000 = models.PositiveIntegerField()
    bills_5000 = models.PositiveIntegerField()
    bills_2000 = models.PositiveIntegerField()


class TransactionLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

