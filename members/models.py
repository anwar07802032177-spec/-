from django.db import models
from django.urls import reverse
from django.utils import timezone


class Member(models.Model):
    """عضو في الجمعية"""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'نشط'
        SUSPENDED = 'suspended', 'موقوف'
        WITHDRAWN = 'withdrawn', 'منسحب'

    class MemberType(models.TextChoices):
        REGULAR = 'regular', 'عادي'
        HONORARY = 'honorary', 'شرفي'
        FOUNDER = 'founder', 'مؤسس'

    membership_number = models.CharField('رقم العضوية', max_length=20, unique=True)
    full_name = models.CharField('الاسم الكامل', max_length=150)
    national_id = models.CharField('رقم البطاقة الوطنية', max_length=20, blank=True)
    phone = models.CharField('الهاتف', max_length=20, blank=True)
    email = models.EmailField('البريد الإلكتروني', blank=True)
    address = models.TextField('العنوان', blank=True)
    photo = models.ImageField('الصورة', upload_to='members/photos/', blank=True, null=True)

    member_type = models.CharField(
        'نوع العضوية', max_length=20,
        choices=MemberType.choices, default=MemberType.REGULAR,
    )
    status = models.CharField(
        'الحالة', max_length=20,
        choices=Status.choices, default=Status.ACTIVE,
    )
    join_date = models.DateField('تاريخ الانخراط', default=timezone.now)
    notes = models.TextField('ملاحظات', blank=True)

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'الأعضاء'
        ordering = ['membership_number']

    def __str__(self):
        return f'{self.membership_number} - {self.full_name}'

    def get_absolute_url(self):
        return reverse('member_detail', args=[self.pk])


class Subscription(models.Model):
    """اشتراك سنوي لعضو"""

    class PaymentStatus(models.TextChoices):
        PAID = 'paid', 'مدفوع'
        UNPAID = 'unpaid', 'غير مدفوع'

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE,
        related_name='subscriptions', verbose_name='العضو',
    )
    year = models.PositiveIntegerField('السنة')
    amount = models.DecimalField('المبلغ', max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        'حالة الدفع', max_length=20,
        choices=PaymentStatus.choices, default=PaymentStatus.UNPAID,
    )
    payment_date = models.DateField('تاريخ الدفع', blank=True, null=True)
    notes = models.CharField('ملاحظات', max_length=255, blank=True)

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = 'اشتراك'
        verbose_name_plural = 'الاشتراكات'
        ordering = ['-year', 'member']
        unique_together = ('member', 'year')

    def __str__(self):
        return f'{self.member.full_name} - {self.year}'
