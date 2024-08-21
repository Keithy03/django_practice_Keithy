from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .form import CustomerForm, LoginForm, TransactionForm, EditCustomerForm
from .models import Customer, TransactionLog


# BEGGING CUSTOMERS


def loginOffice(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['name'], password=request.POST['pin'])
        if user is not None:
            login(request, user)
            return redirect('atm:customer')
        else:
            messages.error(request, 'Username and password did not match')
            form = LoginForm().as_grid()
            return render(request, 'atm/customers/loginCustomers.html', {'form': form})
    else:
        form = LoginForm().as_grid()
        return render(request, 'atm/customers/loginCustomers.html', {'form': form})


def logoutOffice(request):
    logout(request)
    return redirect('atm:index')


@permission_required('atm.can_manage_client')
def indexCustomer(request):
    customers = Customer.objects.all()
    return render(request, "atm/customers/customersList.html", {"customers": customers})


@permission_required('atm.can_manage_client')
def createCustomer(request):
    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("atm:customer")
    return render(request, "atm/customers/createCustomer.html", {"form": form})


@permission_required('atm.can_manage_client')
def editCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = EditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer.save()
            return redirect("atm:customer")
    else:
        # Load data into the form.
        form = EditCustomerForm(instance=customer)

    return render(request, "atm/customers/editCustomer.html", {'form': form, 'customer': customer})


@permission_required('atm.can_manage_client')
def deleteCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect("atm:customer")

    return render(request, 'atm/customers/deleteCustomer.html', {'customer': customer})

# END CUSTOMERS


# BEGGING TRANSACTION
def transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            pin = form.cleaned_data['pin']
            amount = form.cleaned_data['amount']
            customer = Customer.objects.filter(pin=pin).first()
            if customer:
                if customer.money >= amount:
                    if calculateBills(amount):
                        bills = calculateBills(amount)
                        customer.money -= amount
                        customer.save()
                        newTransaction = TransactionLog.objects.create(
                            customer = customer,
                            amount = amount
                        )

                        message = generateMessage(bills)
                        return render(request, "atm/transactionResult.html", {'message': message, 'customer': customer})
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
    return render(request, "atm/transactionLogs.html", {'transactionLogs': transactionLogs})

# END TRANSACTION
