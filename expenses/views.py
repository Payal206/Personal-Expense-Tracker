from django.shortcuts import render,  redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import TransactionForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
@login_required
def dashboard(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')

    income = transactions.filter(
        transaction_type='Income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense = transactions.filter(
        transaction_type='Expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = income - expense
    category_summary = list(
    Transaction.objects.filter(
        user=request.user,
        transaction_type='Expense'
    ).values('category').annotate(
        total=Sum('amount')
    )
)
    monthly_expenses = Transaction.objects.filter(
    user=request.user,
    transaction_type='Expense'
).annotate(
    month=TruncMonth('date')
).values('month').annotate(
    total=Sum('amount')
).order_by('month')
    context = {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
        'category_summary': category_summary,
        'monthly_expenses': monthly_expenses,
    }

    return render(
        request,
        'expenses/dashboard.html',
         context,
    )
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = UserCreationForm()

    return render(request, 'expenses/register.html', {'form': form})
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'expenses/add_transaction.html', {
        'form': form
    })
@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        'expenses/edit_transaction.html',
        {'form': form}
    )
@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')

    return render(
        request,
        'expenses/delete_transaction.html',
        {'transaction': transaction}
    )