from django.conf.urls import url
from django.urls import path, include
from accounts.views import (
    signup, 
    login, 
    logout,
    email_verification,
    resend_email_verification,
    )

# URL Pattern for the account -login-logout-signup
urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('email-verification/<str:uidb64>/<str:token>',email_verification, name='email_verification'),
    path('resend-email-verification', resend_email_verification, name='resend_email_verification'),
]
