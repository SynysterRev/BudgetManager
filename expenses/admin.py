from django.contrib import admin

from expenses.models import Category, Transaction

admin.site.register(Category)
admin.site.register(Transaction)
