from django.urls import path

from atm.views import inicio, indexCustomer, createCustomer, editCustomer, loginCustomers, transaction

urlpatterns = [
    path('', inicio, name="index"),

    # Customers
    path('login', loginCustomers, name="loginCustomer"),
    path('customers/', indexCustomer, name="customer"),
    path('customers/create', createCustomer, name="createCustomer"),
    path('customers/edit/<int:pk>', editCustomer, name="editCustomer"),

    # Transaction
    path('transaction/', transaction, name="transaction"),

]
