from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name

    class Meta:
        permissions = [('can_manage_client', 'Can manage client')]

class Customer(models.Model):
    name = models.CharField(max_length=50)
    pin = models.CharField(max_length=5)
    money = models.IntegerField()

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.money, self.pin)


class TransactionLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.customer.name} of amount {self.amount}"

