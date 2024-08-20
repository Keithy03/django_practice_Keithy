from django.contrib import admin

from atm.models import Customer, Transaction, ATM, TransactionLog


admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(ATM)
admin.site.register(TransactionLog)
