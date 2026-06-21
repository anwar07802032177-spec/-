from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TransactionForm
from .models import Category, Transaction


def _balance(qs=None):
    """حساب الرصيد = مجموع المداخيل - مجموع المصاريف"""
    qs = qs if qs is not None else Transaction.objects.all()
    income = qs.filter(kind=Transaction.Kind.INCOME).aggregate(s=Sum('amount'))['s'] or 0
    expense = qs.filter(kind=Transaction.Kind.EXPENSE).aggregate(s=Sum('amount'))['s'] or 0
    return income, expense, income - expense


@login_required
def transaction_list(request):
    transactions = Transaction.objects.select_related('category', 'member')
    kind = request.GET.get('kind', '').strip()
    if kind in ('income', 'expense'):
        transactions = transactions.filter(kind=kind)

    income, expense, balance = _balance()  # الرصيد الكلي دائماً

    context = {
        'transactions': transactions,
        'kind': kind,
        'total_income': income,
        'total_expense': expense,
        'balance': balance,
    }
    return render(request, 'finance/transaction_list.html', context)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة العملية المالية بنجاح.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(initial={'date': timezone.now().date()})
    return render(request, 'finance/transaction_form.html',
                  {'form': form, 'title': 'إضافة عملية مالية'})


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث العملية المالية.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'finance/transaction_form.html',
                  {'form': form, 'title': 'تعديل عملية مالية'})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'تم حذف العملية المالية.')
        return redirect('transaction_list')
    return render(request, 'finance/transaction_confirm_delete.html',
                  {'transaction': transaction})


@login_required
def financial_report(request):
    """تقرير مالي: تجميع حسب الفئة لسنة مختارة"""
    year = request.GET.get('year', '').strip()
    qs = Transaction.objects.all()
    if year.isdigit():
        qs = qs.filter(date__year=int(year))
        selected_year = int(year)
    else:
        selected_year = timezone.now().year
        qs = qs.filter(date__year=selected_year)

    income, expense, balance = _balance(qs)

    # تجميع حسب الفئة
    by_category = (
        qs.values('category__name', 'kind')
        .annotate(total=Sum('amount'))
        .order_by('kind', '-total')
    )

    # السنوات المتوفرة
    years = (
        Transaction.objects.dates('date', 'year', order='DESC')
    )

    context = {
        'selected_year': selected_year,
        'total_income': income,
        'total_expense': expense,
        'balance': balance,
        'by_category': by_category,
        'years': [d.year for d in years],
    }
    return render(request, 'finance/report.html', context)
