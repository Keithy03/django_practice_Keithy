from django.contrib import admin

from atm.models import Customer, TransactionLog, User

admin.site.register(Customer)
admin.site.register(User)
admin.site.register(TransactionLog)
