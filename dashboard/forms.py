from django.utils import timezone
from datetime import datetime
from django import forms
from django.forms import ModelForm
from dashboard import models
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()


class LoanCreationForm(ModelForm):
    account_name = forms.CharField(required=True)
    account_number = forms.IntegerField(required=True)
    bank_name = forms.CharField(required=True)
    amount = forms.CharField(required=True)

    class Meta:
        model = models.Loan
        fields = (
            'account_name',
            'account_number',
            'bank_name',
            'amount',
        )

    def save(self, commit=True):
        request_loan = super(LoanCreationForm, self).save(commit=False)
        request_loan.account_name = (self.cleaned_data['account_name'])
        request_loan.account_number = self.cleaned_data['account_number']
        request_loan.bank_name = self.cleaned_data['bank_name']
        request_loan.amount = self.cleaned_data['amount']
        request_loan.created_at = timezone.datetime.now()
        request_loan.updated_at = timezone.datetime.now()

        if commit:
            request_loan.save()

        return request_loan


class RepaymentCreationForm(ModelForm):
    description = forms.CharField(required=True)
    amount = forms.CharField(required=True)
    repayment_img = forms.ImageField()
    
    class Meta:
        model = models.Repayment
        fields = (
            'description',
            'amount',
            'repayment_img',
        )

    def save(self, commit=True):
        add_repayment = super(RepaymentCreationForm, self).save(commit=False)
        add_repayment.description = self.cleaned_data['description']
        add_repayment.amount = self.cleaned_data['amount']
        add_repayment.repayment_img = self.cleaned_data['repayment_img']
        add_repayment.created_at = timezone.datetime.now()
        add_repayment.updated_at = timezone.datetime.now()

        if commit:
            add_repayment.save()

            return add_repayment
