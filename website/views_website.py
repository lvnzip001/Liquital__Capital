from django.shortcuts import render
import http
from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def careers(request):
    return render(request, "careers.html")


def milestones(request):
    return render(request, "milestones.html")

def about_us(request):
    return render(request, "about_us.html")


def contact_us(request):
    return render(request, "contact_us.html")

def faq(request):
    return render(request, "faq.html")


def preapproval_application_1(request):
    return render(request, "preapproval_application_1.html")






