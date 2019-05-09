from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext

# View for the home Page
def home(request):
    return render(request, 'home.html')
