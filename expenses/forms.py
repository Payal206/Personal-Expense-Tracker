from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'category', 'transaction_type', 'date']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }