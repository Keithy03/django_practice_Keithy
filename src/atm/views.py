from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .form import LoginForm, TransactionForm, CLientForm, AccountForm
from .models import Client, Account, TransactionLog


# ****    EXAMPLE LOGIN    ****
def loginOffice(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['name'], password=request.POST['pin'])
        if user is not None:
            login(request, user)
            return redirect('atm:customer')
        else:
            messages.error(request, 'Username and password did not match')
            form = LoginForm().as_grid()
            return render(request, 'atm/client/loginCustomers.html', {'form': form})
    else:
        form = LoginForm().as_grid()
        return render(request, 'atm/client/loginCustomers.html', {'form': form})

def logoutOffice(request):
    logout(request)
    return redirect('atm:index')


# ****    BEGGING CLIENTS    ****
# ****    WITH GENERIC VIEWS    ****

# It is used to give you specific permission.
class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'atm/client/client_list.html'
    queryset = Client.objects.all()
    context_object_name = 'clients'
    permission_required = 'atm.can_manage_client'


class CreateClientView(PermissionRequiredMixin, CreateView):
    form_class = CLientForm
    template_name = 'atm/client/create_client.html'
    success_url = reverse_lazy('atm:clients')
    permission_required = 'atm.can_manage_client'


class EditClientView(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = CLientForm
    template_name = 'atm/client/edit_client.html'
    success_url = reverse_lazy('atm:clients')
    permission_required = 'atm.can_manage_client'

class DeleteClientView(PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'atm/client/delete_client.html'
    success_url = reverse_lazy('atm:clients')
    permission_required = 'atm.can_manage_client'
# ****    END WITH GENERIC VIEWS    ****

# ****    EXAMPLE WITHOUT GENERIC VIEWS    ****
@permission_required('atm.can_manage_client')
def indexClients(request):
    clients = Client.objects.all()
    return render(request, "atm/client/client_list.html", {"clients": clients})

@permission_required('atm.can_manage_client')
def createClient(request):
    form = CLientForm()

    if request.method == "POST":
        form = CLientForm(request.POST)
        if form.is_valid():
            form.save()
            # message = "A client was successfully created"
            return redirect("atm:clients")
    return render(request, "atm/client/create_client.html", {"form": form})

@permission_required('atm.can_manage_client')
def editClient(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = CLientForm(request.POST, instance=client)
        if form.is_valid():
            client.save()
            return redirect("atm:clients")
    else:
        # Load data into the form.
        form = CLientForm(instance=client)

    return render(request, "atm/client/edit_client.html", {'form': form, 'client': client})

@permission_required('atm.can_manage_client')
def deleteClient(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()
        return redirect("atm:clients")

    return render(request, 'atm/client/delete_client.html', {'client': client})
# ****    END CLIENTS    ****


# ****    BEGGING ACCOUNTS    ****
class AccountListView(PermissionRequiredMixin, ListView):
    model = Account
    template_name = 'atm/account/account_list.html'
    queryset = Account.objects.all()
    context_object_name = 'accounts'
    permission_required = 'atm.can_manage_client'

class CreateAccountView(PermissionRequiredMixin, CreateView):
    form_class = AccountForm
    template_name = 'atm/account/create_account.html'
    success_url = reverse_lazy('atm:accounts')
    permission_required = 'atm.can_manage_client'

class EditAccountView(PermissionRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'atm/account/edit_account.html'
    success_url = reverse_lazy('atm:accounts')
    permission_required = 'atm.can_manage_client'

class DeleteAccountView(PermissionRequiredMixin, DeleteView):
    model = Account
    template_name = 'atm/account/delete_account.html'
    success_url = reverse_lazy('atm:accounts')
    permission_required = 'atm.can_manage_client'
# ****    END ACCOUNTS    ****


# ****    BEGGING TRANSACTION    ****
def transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            pin = form.cleaned_data['pin']
            amount = form.cleaned_data['amount']
            account = Account.objects.filter(pin=pin).first()
            if account:
                if account.money >= amount:
                    if calculateBills(amount):
                        bills = calculateBills(amount)
                        account.money -= amount
                        account.save()
                        newTransaction = TransactionLog.objects.create(
                            account=account,
                            amount=amount,
                            type='Money withdrawal'
                        )

                        message = generateMessage(bills)
                        return render(request, "atm/transaction_result.html", {'message': message, 'account': account})
                    else:
                        return render(request, "atm/transaction.html",
                                      {"form": TransactionForm(),
                                       'error': 'Cannot provide the exact amount with available bills.'})
                else:
                    return render(request, "atm/transaction.html",
                                  {"form": TransactionForm(), 'error': 'Insufficient funds.'})
            else:
                return render(request, "atm/transaction.html", {"form": TransactionForm(), 'error': 'Invalid PIN.'})

    return render(request, "atm/transaction.html", {"form": TransactionForm()})


def calculateBills(amount):
    bills = {10000: 0, 5000: 0, 2000: 0}

    if amount >= 10000:
        bills[10000] = amount // 10000
        amount %= 10000

    if amount >= 5000:
        bills[5000] = amount // 5000
        amount %= 5000

    if amount >= 2000:
        bills[2000] = amount // 2000
        amount %= 2000

    if amount != 0:
        return None

    return bills


def generateMessage(bills):
    message = []

    for denomination, count in bills.items():
        if count > 0:
            message.append(f"{count} bills of {denomination:,} colones")

    return f"Your money is " + ", ".join(message)


class TransactionLogListView(PermissionRequiredMixin, ListView):
    model = TransactionLog
    template_name = 'atm/transaction_logs.html'
    queryset = TransactionLog.objects.all()
    context_object_name = 'transactionLogs'
    permission_required = 'atm.can_manage_client'
# END TRANSACTION
