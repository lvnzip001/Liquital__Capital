from django.shortcuts import render
import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")

def data_input(request):
    return render(request, "data_input.html")