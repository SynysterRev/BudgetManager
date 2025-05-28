from django import forms

from expenses.default import DEFAULT_COLORS
from expenses.models import Category
from widgets.widgets import InputWidget, ColorPickerWidget


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
