from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

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

        context['categories'] = Category.objects.filter(user=self.request.user)
        return context
