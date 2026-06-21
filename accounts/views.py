from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from finance.models import Transaction
from members.models import Member, Subscription


@login_required
def dashboard(request):
    """لوحة القيادة: إحصائيات سريعة"""
    current_year = timezone.now().year
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status=Member.Status.ACTIVE).count()
    unpaid = Subscription.objects.filter(
        year=current_year, payment_status=Subscription.PaymentStatus.UNPAID
    ).count()
    latest_members = Member.objects.order_by('-created_at')[:5]

    # الرصيد المالي
    income = Transaction.objects.filter(
        kind=Transaction.Kind.INCOME).aggregate(s=Sum('amount'))['s'] or 0
    expense = Transaction.objects.filter(
        kind=Transaction.Kind.EXPENSE).aggregate(s=Sum('amount'))['s'] or 0
    balance = income - expense

    context = {
        'total_members': total_members,
        'active_members': active_members,
        'unpaid_subscriptions': unpaid,
        'current_year': current_year,
        'latest_members': latest_members,
        'total_income': income,
        'total_expense': expense,
        'balance': balance,
    }
    return render(request, 'accounts/dashboard.html', context)
