from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from accounts.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .tokens import account_activation_token





# Create your views here.


# Process and redirect login form data
def login(request):
    # if you are logged-in you shouldnt be able to visit the login URL
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            # Authenticate users input and match it to our database record and return a response
            user = auth.authenticate(
                email=(request.POST['email']).casefold(),
                password=request.POST['password']
            )
            # if find match, take the user to our dashboard page
            if user is not None:
                if user.email_confirmed:
                    auth.login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Account has not been activated, please activate through the link sent to your email!')
                    context = {'resend':'resend'}
                    return render(request, 'accounts/login.html', context)
            # if we couldnt find a match take them back to the login page with the error 
            else:
                messages.error(request, 'Email or password do not match our record')
                return render(request, 'accounts/login.html')
        else:
            return render(request, 'accounts/login.html')


def signup(request):
    # if you are logged-in you shouldnt be able to visit the signup URL
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid(): 
                # form is a valid response then save the data               
                user = User.objects.create_user(
                    email=(form.cleaned_data['email']).casefold(),
                    password=form.cleaned_data['password1'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_no=form.cleaned_data['phone_no'],
                    bvn=form.cleaned_data['bvn'],
                )

                # send_mail(subject, message, from_email, to_list, fail_silently=True)
                subject = 'QuickCash Email Verification'

                current_site = "http://127.0.0.1:8000/accounts/email-verification" 
                # current_site = get_current_site(request)
                uid = (user.pk)
                token = account_activation_token.make_token(user)

                token_verification = User.objects.get(pk=user.pk)
                token_verification.activation_token = token
                token_verification.save()

                activation_link = "{0}/{1}/{2}".format(current_site, uid, token)
                message = "Hello {0},\n \n {1}".format((user.first_name).capitalize(), activation_link)

                # message = 'Welcome to Quickcash Loan. In order to gain full access to our website please activate your account with the link below.'
                from_email = settings.EMAIL_HOST_USER
                to_list = [(form.cleaned_data['email']).casefold(), settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list)

                # auth.login(request, user)
                # return redirect('dashboard')
                messages.success(request, 'Account creation was successful. Please, activate your account through the confirmation email sent to your email')
                context = {'resend':'resend'}
                return render(request, 'accounts/login.html', context)
            else:
                # Form has error relay the error to the user
                context = {'form':form}
                return render(request, 'accounts/signup.html', context)
        else:
            return render(request, 'accounts/signup.html')


def email_verification(request, uidb64, token):
    try:
        uid = (uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {'resend':'resend'}
    if user is not None and user.activation_token == token:
        user.email_confirmed = True
        user.activation_token = "active"
        user.save()
        messages.success(request, 'Thank you. Your account has been verified. Now you can login to your account.')
        return redirect('login')
    else:
        if user.email_confirmed:
            messages.error(request, 'This link has expired. Please login.')
            return render(request, 'accounts/login.html', context)
        messages.error(request, 'Activation link is invalid!')        
        return render(request, 'accounts/login.html', context)


def resend_email_verification(request):
    if request.method == 'POST': 
        try:
            email = (request.POST['email']).casefold()
            user = User.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        context = {'resend':'resend'}
        if user is not None:

            if user.email_confirmed:
                messages.error(request, 'Account already activated, please login.')
                return redirect('login')

            # send_mail(subject, message, from_email, to_list, fail_silently=True)
            subject = 'QuickCash Email Verification'

            current_site = "http://127.0.0.1:8000/accounts/email-verification"
            # current_site = get_current_site(request)
            uid = (user.pk)
            token = account_activation_token.make_token(user)

            token_verification = User.objects.get(pk=user.pk)
            token_verification.activation_token = token
            token_verification.save()

            activation_link = "{0}/{1}/{2}".format(
                current_site, uid, token)
            message = "Hello {0},\n \n {1}".format(
                (user.first_name).capitalize(), activation_link)

            # message = 'Welcome to Quickcash Loan. In order to gain full access to our website please activate your account with the link below.'
            from_email = settings.EMAIL_HOST_USER
            to_list = [(request.POST['email']).casefold(),
                        settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list)

            messages.success(request, 'Activation link has been sent to your Email. Please, activate your account through the link.')
            return render(request, 'accounts/login.html', context)
        else:
            messages.error(request, 'Email do not match our record!')
            return render(request, 'accounts/login.html', context)



# The logout function, kills all active session
@login_required(login_url="/accounts/login")
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
