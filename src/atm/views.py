from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404

from .form import LoginForm, TransactionForm, CLientForm, AccountForm
from .models import Client, Account, TransactionLog


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

# ****    BEGGING CLIENTS    ****
def logoutOffice(request):
    logout(request)
    return redirect('atm:index')


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
@permission_required('atm.can_manage_client')
def indexAccounts(request):
    accounts = Account.objects.all()
    return render(request, "atm/client/account/account_list.html", {"accounts": accounts})

@permission_required('atm.can_manage_client')
def createAccount(request):
    form = AccountForm()
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            # message = "A client was successfully created"
            return redirect("atm:accounts")
    return render(request, "atm/client/account/create_account.html", {"form": form})


@permission_required('atm.can_manage_client')
def editAccount(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account.save()
            return redirect("atm:accounts")
    else:
        # Load data into the form.
        form = AccountForm(instance=account)

    return render(request, "atm/client/account/edit_account.html", {'form': form, 'account': account})


@permission_required('atm.can_manage_client')
def deleteAccount(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        account.delete()
        return redirect("atm:accounts")

    return render(request, 'atm/client/account/delete_account.html', {'account': account})

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
                            account = account,
                            amount = amount,
                            type = 'Money withdrawal'
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


@permission_required('atm.can_manage_client')
def viewTransactionLogs(request):
    transactionLogs = TransactionLog.objects.all()
    return render(request, "atm/transaction_logs.html", {'transactionLogs': transactionLogs})

# END TRANSACTION
