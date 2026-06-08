from django import forms
from django.db import models
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 '
                             'rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 '
                             'focus:ring-2 focus:ring-blue-500 focus:outline-none',
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter amount($)',
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 '
                             'rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 '
                             'focus:ring-2 focus:ring-blue-500 focus:outline-none',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Optional description...',
                    'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 '
                             'rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 '
                             'focus:ring-2 focus:ring-blue-500 focus:outline-none',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = Category.objects.filter(
                models.Q(user=user) | models.Q(user=None)
            )
