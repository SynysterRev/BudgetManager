from datetime import date
from decimal import Decimal

from django import forms

from expenses.default import DEFAULT_COLORS
from expenses.models import Category, Transaction
from widgets.widgets import InputWidget, ColorPickerWidget, DropdownWidget, RadioWidget, \
    DatePickerWidget


class CreateTransactionForm(forms.ModelForm):
    amount = forms.CharField(
        widget=InputWidget(attrs={
            "pattern": r"[0-9]+([.,][0-9]{1,2})?",
            "placeholder": "0.00",
            "title": "Amount",
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        self.fields["category"].widget = DropdownWidget(
            attrs={
                "title": "Category",
                "options": Category.objects.filter(user=self.user)
            }
        )
        self.fields["datetime"].initial = date.today()


    class Meta:
        model = Transaction
        fields = ["description", "amount", "category", "datetime", "transaction_type"]
        widgets = {
            "description": InputWidget(
                attrs={
                    "title": "Description",
                    "placeholder": "E.g., Monthly Rent",
                    "type": "text",
                }
            ),
            "transaction_type": RadioWidget(
                choices=Transaction.TRANSACTION_TYPES,
                attrs={
                    "title": "Type",
                }
            ),
            "datetime": DatePickerWidget(
                attrs={
                    "title": "Date",
                }
            )
        }


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if isinstance(amount, str):
            amount_clean = amount.replace(',', '.').strip()
            try:
                return Decimal(amount_clean)
            except:
                raise forms.ValidationError("Invalid format")
        return amount


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]
        widgets = {
            "name": InputWidget(
                attrs={
                    "title": "Category Name",
                    "placeholder": "E.g., Groceries",
                    "type": "text",
                }
            ),
            "color": ColorPickerWidget(
                attrs={
                    "title": "Color",
                    "colors": [color for color in DEFAULT_COLORS]
                }
            )
        }
