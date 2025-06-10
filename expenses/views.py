import csv
import datetime
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Case, When, F, DecimalField
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, \
    UpdateView

from expenses.forms import CreateCategoryForm, CreateTransactionForm
from expenses.mixins import TransactionFilterMixin
from expenses.models import Transaction, Category


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "expenses/dashboard.html"
    model = Transaction
    context_object_name = "transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.datetime.today()

        transactions = Transaction.objects.filter(user=self.request.user,
                                                  datetime__year=current_date.year)

        monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        for t in transactions:
            month = t.datetime.month
            if t.transaction_type == 'income':
                monthly_data[month]['income'] += t.amount
            else:
                monthly_data[month]['expense'] += t.amount

        context['monthly_income'] = monthly_data[current_date.month]['income']
        context['monthly_expense'] = monthly_data[current_date.month]['expense']
        context['monthly_balance'] = (monthly_data[current_date.month]['income'] -
                                      monthly_data[current_date.month]['expense'])

        last_month_date = current_date - relativedelta(months=1)
        previous_month_transactions = list(Transaction.objects.filter(
            user=self.request.user,
            datetime__year=last_month_date.year,
            datetime__month=last_month_date.month))
        previous_month_income = sum(t.amount for t in previous_month_transactions if
                                    t.transaction_type == 'income')
        previous_month_expense = sum(t.amount for t in previous_month_transactions if
                                     t.transaction_type == 'expense')

        previous_balance = previous_month_income - previous_month_expense

        context['percent_previous_balance'] = round(((context['monthly_balance'] -
                                                      previous_balance) / previous_balance)
                                                    * 100) if (
                previous_balance != 0) else 100

        context['percent_previous_income'] = round(((context['monthly_income'] -
                                                     previous_month_income) /
                                                    previous_month_income) * 100) if (
                previous_month_income != 0) else 100

        context['percent_previous_expense'] = round(((context['monthly_expense'] -
                                                      previous_month_expense) /
                                                     previous_month_expense) * 100) if (
                previous_month_expense != 0) else 100
        if context['percent_previous_balance'] > 0:
            context['diff_balance_class'] = 'text-success'
            context['diff_balance_icon'] = '↑'
        else:
            context['diff_balance_class'] = 'text-alert'
            context['diff_balance_icon'] = '↓'

        if context['percent_previous_income'] > 0:
            context['diff_income_class'] = 'text-success'
            context['diff_income_icon'] = '↑'
        else:
            context['diff_income_class'] = 'text-alert'
            context['diff_income_icon'] = '↓'

        if context['percent_previous_expense'] < 0:
            context['diff_expense_class'] = 'text-success'
            context['diff_expense_icon'] = '↓'
        else:
            context['diff_expense_class'] = 'text-alert'
            context['diff_expense_icon'] = '↑'

        return context

    def get_queryset(self):
        return Transaction.objects.order_by("datetime")[:5]


class ExpenseView(LoginRequiredMixin, TransactionFilterMixin, ListView):
    model = Transaction
    template_name = "expenses/expense_page.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_types'] = Transaction.TRANSACTION_TYPES

        categories = Category.objects.filter(user=self.request.user)
        context['categories'] = [category.name for category in categories]

        balance = Transaction.objects.filter(user=self.request.user).aggregate(
            balance=Sum(
                Case(
                    When(transaction_type='expense', then=-F('amount')),
                    When(transaction_type='income', then=F('amount')),
                    default=0,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )['balance'] or Decimal('0.00')

        context['balance'] = balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return context

    def get_queryset(self):
        return self.get_filtered_queryset(self.request)


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "expenses/partials/create_transaction.html"
    form_class = CreateTransactionForm
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        if self.request.method == "POST":
            return JsonResponse({
                'success': True,
                'message': 'Transaction created successfully!'
            }, status=200)

        return response

    def form_invalid(self, form):
        if self.request.method == "POST":
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ExpenseEditView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = CreateTransactionForm
    template_name = "expenses/partials/create_transaction.html"
    success_url = reverse_lazy('expenses')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self, queryset=...):
        return Transaction.objects.get(user=self.request.user, id=self.kwargs[
            "expense_id"])

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.method == "POST":
            return JsonResponse({
                'success': True,
                'message': 'Transaction created successfully!'
            }, status=200)

        return response

    def form_invalid(self, form):
        if self.request.method == "POST":
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('expenses')

    def get_object(self, queryset=...):
        return Transaction.objects.get(user=self.request.user, id=self.kwargs[
            "expense_id"])


class ExpenseExportCSV(LoginRequiredMixin, TransactionFilterMixin, View):
    def get(self, request, *args, **kwargs):
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        csv_name = f"transactions-{today_date}.csv"
        response = HttpResponse(content_type="text/csv",
                                headers={
                                    "Content-Disposition": f"attachment; filename= {csv_name}"}, )

        writer = csv.writer(response)
        writer.writerow(["Date", "Description", "Category", "Type", "Amount"])
        transactions = self.get_filtered_queryset(self.request)
        for transaction in transactions:
            writer.writerow([transaction.datetime, transaction.description,
                             transaction.category, transaction.transaction_type,
                             transaction.amount])

        return response


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "expenses/category_page.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "expenses/partials/create_category.html"
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "expenses/partials/create_category.html"
    success_url = reverse_lazy('categories')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_object(self, queryset=...):
        return Category.objects.get(user=self.request.user, name=self.kwargs["name"])


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_object(self, queryset=...):
        return Category.objects.get(user=self.request.user, name=self.kwargs["name"])
