from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class OfficeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name

    class Meta:
        permissions = [('can_manage_client', 'Can manage client')]


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    dni = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=CASCADE)
    pin = models.IntegerField(unique=True)
    money = models.IntegerField()

    def __str__(self):
        return "%s - %s - %s" % (self.client.name, self.money, self.pin)

class Customer(models.Model):
    name = models.CharField(max_length=50)
    pin = models.IntegerField(unique=True)
    money = models.IntegerField()

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.money, self.pin)


class TransactionLog(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=15)

    def __str__(self):
        return f"Transaction by {self.account.client.name} of amount {self.amount}"