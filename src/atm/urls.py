from django.urls import path

from atm.views import indexCustomer, createCustomer, editCustomer, transaction, deleteCustomer, \
    loginOffice, logoutOffice, viewTransactionLogs

app_name= 'atm'
urlpatterns = [
    # Transaction
    path('', transaction, name="index"),
    path('transaction', transaction, name="transaction"),
    path('transactionLogs', viewTransactionLogs, name="transactionLog"),

    # Customers
    path('customers/', indexCustomer, name="customer"),
    path('customers/create', createCustomer, name="createCustomer"),
    path('customers/edit/<int:pk>', editCustomer, name="editCustomer"),
    path('customers/delete/<int:pk>', deleteCustomer, name="deleteCustomer"),

]
