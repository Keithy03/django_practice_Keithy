from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from .form import CustomerForm, LoginForm, TransactionForm
from .models import Customer


def inicio(request):
    return render(request, "atm/indexATM.html", )


# BEGGING CUSTOMERS

# More things neet to be contemplated
def loginCustomers(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pin = form.cleaned_data['pin']
            customer = Customer.objects.filter(name=name, pin=pin).first()
            if customer and customer.user_type == 2:
                return redirect('customer')
    else:
        form = LoginForm()
    return render(request, "atm/customers/loginCustomers.html", {'form': form})


def indexCustomer(request):
    customers = Customer.objects.all()
    return render(request, "atm/customers/crudCustomers.html", {"customers": customers})


def createCustomer(request):
    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer")
    return render(request, "atm/customers/createCustomer.html", {"form": form})


# Not Working
def editCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer")
    else:
        form = CustomerForm(instance=customer)

    return render(request, "atm/customers/editCustomer.html", {'form': form, 'customer': customer})


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
                    bills = calculateBills(amount)

                    if bills:
                        message = generateMessage(bills)
                        return render(request, "atm/transactionResult.html", {'message': message})
                    else:
                        return render(request, "atm/transactionResult.html",
                                      {'error': 'Cannot provide the exact amount with available bills.'})
                else:
                    return render(request, "atm/transactionResult.html", {'error': 'Insufficient funds.'})
            else:
                return render(request, "atm/transactionResult.html", {'error': 'Invalid PIN.'})

    else:
        form = TransactionForm()

    return render(request, "atm/transaction.html", {"form": form})


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

    return bills


def generateMessage(bills):
    message = []

    for denomination, count in bills.items():
        if count > 0:
            message.append(f"{count} billete{'s' if count > 1 else ''} de {denomination:,} colones")

    return f"Your money is " + ", ".join(message)

# END TRANSACTION
