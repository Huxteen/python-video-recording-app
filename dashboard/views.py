from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from collections import Counter
from django.shortcuts import render, redirect
from dashboard.forms import (
    LoanCreationForm,
    RepaymentCreationForm,
    )
from dashboard.models import Loan, Repayment
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


# Process and redirect login form data
@login_required(login_url="/accounts/login")
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url="/accounts/login")
def request_loan(request):
    if request.method == "POST":
        form = LoanCreationForm(request.POST)
        user_id = int(request.user.id)
        email = request.user.email
        query_set = Loan.objects.filter(Q(user=user_id) & Q(admin_user=None))
        if query_set.count() > 0:
            messages.error(request, 'Sorry, you have an existing loan request')
            return render(request, 'dashboard/request_loan.html')
        elif form.is_valid():
            request_loan = form.save(commit=False)
            request_loan.user = User(pk=user_id)
            request_loan.admin_user = None
            request_loan.save()

            status = Loan.objects.latest('created_at')

            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            subject = 'You Have A New Loan Request'

            current_site = "http://127.0.0.1:8000/dashboard/approve-loan"
            # current_site = get_current_site(request)
            uid = (status.id)
                    
            activation_link = "{0}/{1}/".format(current_site, uid)
            message = "Hello {0},\n {1}\n \n{2}".format("Admin", subject, activation_link)

            # message = 'Welcome to Quickcash Loan. In order to gain full access to our website please activate your account with the link below.'
            from_email = settings.EMAIL_HOST_USER
            to_list = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list)

            

            messages.success(request, 'Congratulations your loan request has been submitted successfully')
            return render(request, 'dashboard/request_loan.html')
        messages.error(request, 'Something went wrong')
        return render(request, 'dashboard/request_loan.html')
    return render(request, 'dashboard/request_loan.html')


@login_required(login_url="/accounts/login")
def my_loan(request):
    user = int(request.user.id)
    my_loans = Loan.objects.filter(user=user).order_by('-created_at')
    context = {'my_loans':my_loans}
    return render(request, 'dashboard/my_loan.html', context)


@login_required(login_url="/accounts/login")
def approve_loan(request, loan_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.method == "POST":
        status = request.POST['status']
        if status == "approve":
            approve_loan = Loan.objects.get(pk=loan_id)
            if approve_loan is not None:
                approve_loan.approve_or_decline = True
                user = int(request.user.id)
                approve_loan.admin_user = User(pk=user)
                approve_loan.save()
                messages.success(request, 'Loan request has been approved')
                return redirect('view_all_loans')
            messages.error(request, 'Loan data do not exist')
            return redirect('view_all_loans')
        else:
            decline_loan = Loan.objects.get(pk=loan_id)
            if approve_loan is not None:
                user = int(request.user.id)
                decline_loan.admin_user = User(pk=user)
                decline_loan.save()
                messages.error(request, 'Loan has been declined')
                return redirect('view_all_loans')
            messages.error(request, 'Loan data do not exist')
            return redirect('view_all_loans')
    return redirect('view_all_loans')


@login_required(login_url="/accounts/login")
def approve_repayment(request, loan_id):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.method == "POST":
        status = request.POST['status']
        if status == "approve":
            approve_repayment = Loan.objects.get(pk=loan_id)
            approve_repayment.repayment_status = 2
            approve_repayment.save()

            repayment = Repayment.objects.get(loan_id=loan_id)
            user = int(request.user.id)
            repayment.admin_user = User(pk=user)
            repayment.status = 1
            repayment.save()

            messages.success(request, 'Repayment request has been approved')
            return redirect('view_all_repayment')
        else:
            decline_repayment = Loan.objects.get(pk=loan_id)
            decline_repayment.repayment_status = 3
            decline_repayment.save()

            repayment = Repayment.objects.get(loan_id=loan_id)
            user = int(request.user.id)
            repayment.admin_user = User(pk=user)
            repayment.status = 2
            repayment.save()

            messages.error(request, 'Repayment has been declined')
            return redirect('view_all_repayment')
    return redirect('view_all_repayment')


@login_required(login_url="/accounts/login")
def make_repayment(request, loan_id):
    if request.method == "POST":
        add_repayment = Repayment()
        add_repayment.amount = request.POST['amount']
        add_repayment.description = request.POST['description']
        add_repayment.repayment_img = request.FILES['repayment_img']
        add_repayment.loan_id = Loan(pk=loan_id)
        add_repayment.user_id = User(pk=request.user.id)
        add_repayment.created_at = timezone.datetime.now()
        add_repayment.updated_at = timezone.datetime.now()
        add_repayment.save()
    
        update_loan = Loan.objects.get(pk=loan_id)
        update_loan.repayment_status = 1
        update_loan.save()

        messages.success(request, 'Loan repayment has been submitted successfully, waiting for approval from admin.')
        return redirect('my_loan')
    messages.error(request, 'something went wrong.')
    return redirect('my_loan')


@login_required(login_url="/accounts/login")
def view_all_loans(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    all_loans = Loan.objects.all().order_by('-created_at')
    context = {'all_loans': all_loans}
    return render(request, 'dashboard/view_all_loans.html', context)


@login_required(login_url="/accounts/login")
def view_all_repayment(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    all_repayments = Repayment.objects.all().order_by('-created_at')
    context = {'all_repayments': all_repayments}
    return render(request, 'dashboard/view_all_repayment.html', context)


@login_required(login_url="/accounts/login")
def change_image(request):
    data = {'message': 'Something went wrong with your form data',
            'status': 'failed'}
    if request.method == "POST":
        user = request.user.id
        change_image = User.objects.get(pk=user)
        change_image.avatar = request.FILES['avatar']
        change_image.save()
        status = User.objects.get(pk=user)
        data = {
            'message':'Profile image has been updated',
            'status':'success',
            'avatar': str(status.avatar),
        }
    return JsonResponse(data)
        


