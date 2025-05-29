from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView

from expenses.forms import CreateCategoryForm
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
        return Transaction.objects.filter(user=self.request.user)


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "expenses/category_page.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')


class CategoryFormView(LoginRequiredMixin, CreateView):
    form_class = CreateCategoryForm
    template_name = "expenses/partials/create_category.html"
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def get_object(self, queryset = ...):
        return Category.objects.get(user=self.request.user, name=self.kwargs["name"])

