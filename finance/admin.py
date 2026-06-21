from django.contrib import admin

from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('kind',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'kind', 'category', 'amount', 'payment_method', 'member')
    list_filter = ('kind', 'payment_method', 'category', 'date')
    search_fields = ('description', 'member__full_name')
    date_hierarchy = 'date'
    autocomplete_fields = ('member',)
