from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """فئة مالية (تبرعات، اشتراكات، إيجار، أدوات...)"""

    class Kind(models.TextChoices):
        INCOME = 'income', 'مدخول'
        EXPENSE = 'expense', 'مصروف'

    name = models.CharField('اسم الفئة', max_length=100)
    kind = models.CharField('النوع', max_length=10, choices=Kind.choices)

    class Meta:
        verbose_name = 'فئة مالية'
        verbose_name_plural = 'الفئات المالية'
        ordering = ['kind', 'name']
        unique_together = ('name', 'kind')

    def __str__(self):
        return f'{self.name} ({self.get_kind_display()})'


class Transaction(models.Model):
    """عملية مالية: مدخول أو مصروف"""

    class Kind(models.TextChoices):
        INCOME = 'income', 'مدخول'
        EXPENSE = 'expense', 'مصروف'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'نقداً'
        CHECK = 'check', 'شيك'
        TRANSFER = 'transfer', 'تحويل بنكي'

    kind = models.CharField('النوع', max_length=10, choices=Kind.choices)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transactions', verbose_name='الفئة',
    )
    amount = models.DecimalField('المبلغ', max_digits=12, decimal_places=2)
    date = models.DateField('التاريخ', default=timezone.now)
    description = models.CharField('الوصف', max_length=255, blank=True)
    payment_method = models.CharField(
        'طريقة الدفع', max_length=10,
        choices=PaymentMethod.choices, default=PaymentMethod.CASH,
    )
    receipt = models.FileField('الوصل/المرفق', upload_to='finance/receipts/', blank=True, null=True)

    # ربط اختياري بعضو (مثلاً مدخول من اشتراك عضو)
    member = models.ForeignKey(
        'members.Member', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='transactions', verbose_name='العضو المرتبط',
    )

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = 'عملية مالية'
        verbose_name_plural = 'العمليات المالية'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.get_kind_display()}: {self.amount} - {self.date}'

    def get_absolute_url(self):
        return reverse('transaction_list')

    @property
    def signed_amount(self):
        """المبلغ موجباً للمدخول وسالباً للمصروف"""
        return self.amount if self.kind == self.Kind.INCOME else -self.amount
