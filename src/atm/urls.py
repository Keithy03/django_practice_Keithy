from django.urls import path

from atm.views import transaction, viewTransactionLogs, createClient, editClient, indexClients, deleteClient, \
    indexAccounts, \
    createAccount, editAccount, deleteAccount

app_name = 'atm'
urlpatterns = [
    # Transaction
    path('', transaction, name="index"),
    path('transaction', transaction, name="transaction"),
    path('transactionLogs', viewTransactionLogs, name="transactionLog"),

    # Client
    path('clients', indexClients, name="clients"),
    path('clients/create', createClient, name="createClient"),
    path('clients/edit/<int:pk>', editClient, name="editClient"),
    path('clients/delete/<int:pk>', deleteClient, name="deleteClient"),

    # Acount
    path('accounts', indexAccounts, name="accounts"),
    path('accounts/create', createAccount, name="createAccount"),
    path('accounts/edit/<int:pk>', editAccount, name="editAccount"),
    path('accounts/delete/<int:pk>', deleteAccount, name="deleteAccount"),
]
