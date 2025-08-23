from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.orders.models.order import Order
from core.apps.accounts.models import User


class Party(BaseModel):
    STATUS = [
        ('NEW', 'yangi'),
        ('PARTY_IS_MADE', 'partiya qilingan'),
        ("EXPECTED", 'kutilmoqda'),
        ('DRAFT', 'qoralama'),
        ('CANCELLED', 'bekor qilingan'),
        ('PURCHASED', 'sotib olinmoqda'),
        ('PROCESS', 'jarayonda'),
    ]
    PAYMENT_STATUS = (
        ('PAID', "to'langan"),
        ('PARTIALLY', 'qisman'),
        ('NOT_PAID', "to'lanmagan"),
        ('OVERPAID', "ortiqcha to'langan"),
    )
    CONFIRMATION = (
        ('EXPECTED', 'kutilmoqda'),
        ('APPROVER', 'tasdiqlangan'),
        ('REJECTED', 'rad etilgan'),
    )

    number = models.PositiveIntegerField(default=1)
    orders = models.ManyToManyField(Order, related_name='parties', null=True, blank=True)
    mediator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parties')
    # dates
    delivery_date = models.DateField()
    closed_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    payment_date = models.DateField()
    # choices
    status = models.CharField(max_length=20, choices=STATUS, default='NEW')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='NOT_PAID')
    confirmation = models.CharField(max_length=20, choices=CONFIRMATION, default='EXPECTED')
    currency = models.CharField(choices=[('usd', 'usd'), ('uzs', 'uzs')], max_length=3, default='uzs')
    # percentages
    payment_percentage = models.FloatField(null=True, blank=True)
    process = models.FloatField(null=True, blank=True)

    comment = models.TextField(null=True, blank=True)
    audit = models.CharField(
        max_length=20, choices=[('CHECKED', 'tekshirildi'),('PROCESS', 'jarayonda')],
        null=True, blank=True
    )
    audit_comment = models.TextField(null=True, blank=True)
    discount = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    discount_currency = models.CharField(
        max_length=3, choices=[('uzs', 'uzs'), ('usd', 'usd')], default='uzs', null=True, blank=True
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'P - {self.number}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_party = Party.objects.order_by('number').last()
            if last_party:
                self.number = last_party.number + 1
            else:
                self.number = 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Partiya'
        verbose_name_plural = 'Partiyalar'


class PartyAmount(BaseModel):
    party = models.OneToOneField(Party, on_delete=models.CASCADE, related_name='party_amount')
    total_price = models.PositiveBigIntegerField()
    cost_amount = models.PositiveBigIntegerField(default=0)
    calculated_amount = models.PositiveBigIntegerField(default=0)
    paid_amount = models.PositiveBigIntegerField(default=0)
    payment_amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.party} amount'

    class Meta:
        verbose_name = 'Partiya Summasi'
        verbose_name_plural = 'Partiya summalari'
    


class DeletedParty(BaseModel):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='deleted_parties')
    deleted_date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.party} deleted at {self.deleted_date}'
    
    def save(self, *args, **kwargs):
        self.party.is_deleted = True
        self.party.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "O'chirilgan partiya"
        verbose_name_plural = "O'chirilgan partiyalar"