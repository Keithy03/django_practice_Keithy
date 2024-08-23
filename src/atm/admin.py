from django.contrib import admin

from atm.models import OfficeUser, Client, Customer

admin.site.register(OfficeUser)
admin.site.register(Client)
admin.site.register(Customer)
