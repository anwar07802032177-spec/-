from django.contrib import admin

from .models import Member, Subscription


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_number', 'full_name', 'member_type', 'status', 'phone', 'join_date')
    list_filter = ('status', 'member_type', 'join_date')
    search_fields = ('membership_number', 'full_name', 'phone', 'email', 'national_id')
    inlines = [SubscriptionInline]
    date_hierarchy = 'join_date'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('member', 'year', 'amount', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'year')
    search_fields = ('member__full_name', 'member__membership_number')
