from django.contrib import admin

# Register your models here.
from .models import Loan, Repayment

admin.site.register(Loan)
admin.site.register(Repayment)
