from expenses.models import Transaction


class TransactionFilterMixin:
    def get_filtered_queryset(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by(
            'datetime')

        category = request.GET.get("category_type")
        if category:
            transactions = transactions.filter(category__name=category)

        transaction_type = request.GET.get("transaction_type")
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date and end_date:
            transactions = transactions.filter(datetime__range=[start_date, end_date])
        elif start_date:
            transactions = transactions.filter(datetime__gte=start_date)
        elif end_date:
            transactions = transactions.filter(datetime__lte=end_date)

        search = request.GET.get("search")
        if search:
            transactions = transactions.filter(description__icontains=search)

        return transactions
