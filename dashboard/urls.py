from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import (
    dashboard,
    request_loan,
    my_loan,
    approve_loan,
    view_all_loans,
    make_repayment,
    view_all_repayment,
    approve_repayment,
    change_image,

    )

# URL for the dashboard app
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('request-loan', request_loan, name='request_loan'),
    path('my-loan', my_loan, name='my_loan'),
    path('change-image', change_image, name='change_image'),
    path('approve-loan/<int:loan_id>/', approve_loan, name='approve_loan'),
    path('approve-repayment/<int:loan_id>/',
         approve_repayment, name='approve_repayment'),
    path('make-repayment/<int:loan_id>/', make_repayment, name='make_repayment'),
    path('view-all-loans', view_all_loans, name='view_all_loans'),
    path('view-all-repayment', view_all_repayment, name='view_all_repayment'),
]
