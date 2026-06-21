from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

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

    context = {
        'total_members': total_members,
        'active_members': active_members,
        'unpaid_subscriptions': unpaid,
        'current_year': current_year,
        'latest_members': latest_members,
    }
    return render(request, 'accounts/dashboard.html', context)
