from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MemberForm, SubscriptionForm
from .models import Member, Subscription


@login_required
def member_list(request):
    """قائمة الأعضاء مع البحث والفلترة"""
    members = Member.objects.all()
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    if query:
        members = members.filter(
            Q(full_name__icontains=query)
            | Q(membership_number__icontains=query)
            | Q(phone__icontains=query)
            | Q(email__icontains=query)
        )
    if status:
        members = members.filter(status=status)

    context = {
        'members': members,
        'query': query,
        'status': status,
        'status_choices': Member.Status.choices,
        'total': members.count(),
    }
    return render(request, 'members/member_list.html', context)


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'members/member_detail.html', {'member': member})


@login_required
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, 'تمت إضافة العضو بنجاح.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm()
    return render(request, 'members/member_form.html', {'form': form, 'title': 'إضافة عضو'})


@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بيانات العضو بنجاح.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form, 'title': 'تعديل عضو'})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'تم حذف العضو.')
        return redirect('member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': member})


@login_required
def subscription_create(request, member_pk):
    member = get_object_or_404(Member, pk=member_pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة الاشتراك.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = SubscriptionForm(initial={'member': member})
    return render(request, 'members/subscription_form.html',
                  {'form': form, 'member': member, 'title': 'إضافة اشتراك'})
