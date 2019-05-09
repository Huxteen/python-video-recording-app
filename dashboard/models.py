from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='admin_users', default=None, blank=True, null=True)
    account_name = models.CharField(max_length=150)
    account_number = models.IntegerField(blank=True, null=True)
    bank_name = models.CharField(max_length=255)
    amount = models.CharField(max_length=20)
    repayment_status = models.IntegerField(default=0, blank=True, null=True)
    approve_or_decline = models.BooleanField(default=False)   
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.account_name


class Repayment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ids', default=1)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_ids')
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='repayment_admin_users', default=None, blank=True, null=True)
    description = models.CharField(max_length=255)
    amount = models.CharField(max_length=20, default=None)
    status = models.IntegerField(default=0, blank=True, null=True)
    repayment_img = models.ImageField(upload_to='repayment_img/', null=True, blank=True)
    created_at = models.DateTimeField(
        default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(
        default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.description

