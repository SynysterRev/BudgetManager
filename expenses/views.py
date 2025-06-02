import csv
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Case, When, F, DecimalField
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, \
    UpdateView

from expenses.forms import CreateCategoryForm, CreateTransactionForm
from expenses.mixins import TransactionFilterMixin
from expenses.models import Transaction, Category


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "expenses/dashboard.html"


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

        balance = Transaction.objects.aggregate(
            balance=Sum(
                Case(
                    When(transaction_type='expense', then=-F('amount')),
                    When(transaction_type='income', then=F('amount')),
                    default=0,
                    output_field=DecimalField(),
                )
            )
        )['balance'] or 0

        context['balance'] = balance

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
