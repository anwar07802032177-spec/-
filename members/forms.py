from django import forms

from .models import Member, Subscription


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'membership_number', 'full_name', 'national_id',
            'phone', 'email', 'address', 'photo',
            'member_type', 'status', 'join_date', 'notes',
        ]
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['member', 'year', 'amount', 'payment_status', 'payment_date', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }
