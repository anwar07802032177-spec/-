from django import forms

from .models import Category, Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'kind', 'category', 'amount', 'date',
            'description', 'payment_method', 'member', 'receipt',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'kind']
