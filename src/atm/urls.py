from django.urls import path

from atm.views import transaction, createClient, editClient, indexClients, deleteClient, \
    ClientListView, CreateClientView, EditClientView, DeleteClientView, \
    AccountListView, CreateAccountView, EditAccountView, DeleteAccountView, TransactionLogListView

app_name = 'atm'
urlpatterns = [
    # Transaction
    path('', transaction, name="index"),
    path('transaction', transaction, name="transaction"),
    path('transactionLogs', TransactionLogListView.as_view(), name="transactionLog"),

    # Client
    path('clients', ClientListView.as_view(), name="clients"),
    path('clients/create', CreateClientView.as_view(), name="createClient"),
    path('clients/edit/<int:pk>', EditClientView.as_view(), name="editClient"),
    path('clients/delete/<int:pk>', DeleteClientView.as_view(), name="deleteClient"),

    # Acount
    path('accounts', AccountListView.as_view(), name="accounts"),
    path('accounts/create', CreateAccountView.as_view(), name="createAccount"),
    path('accounts/edit/<int:pk>', EditAccountView.as_view(), name="editAccount"),
    path('accounts/delete/<int:pk>', DeleteAccountView.as_view(), name="deleteAccount"),
]
