from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, \
    UpdateView

from expenses.forms import CreateCategoryForm, CreateTransactionForm
from expenses.models import Transaction, Category


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "expenses/dashboard.html"


class ExpenseView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "expenses/expense_page.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_types'] = Transaction.TRANSACTION_TYPES

        categories = Category.objects.filter(user=self.request.user)
        context['categories'] = [category.name for category in categories]
        return context

    def get_queryset(self):
        transactions = Transaction.objects.filter(user=self.request.user).order_by(
            'datetime')
        # page is reloaded every time, check with JS or HTMX to avoid the reloading
        category = self.request.GET.get("category_type")
        if category:
            transactions = transactions.filter(category__name=category)

        transaction_type = self.request.GET.get("transaction_type")
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date and end_date:
            transactions = transactions.filter(datetime__range=[start_date, end_date])
        elif start_date:
            transactions = transactions.filter(datetime__gte=start_date)
        elif end_date:
            transactions = transactions.filter(datetime__lte=end_date)

        return transactions


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
            })

        return response

    def form_invalid(self, form):
        if self.request.method == "POST":
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

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
            })

        return response

    def form_invalid(self, form):
        if self.request.method == "POST":
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

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
