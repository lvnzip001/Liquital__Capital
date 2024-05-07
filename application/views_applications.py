from django.shortcuts import render
import http
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required

def complete_application(request):
    return render(request, "complete_application.html")

def asset_liability_view(request):
    AssetFormset = modelformset_factory(Asset, form=AssetForm, extra=1)
    LiabilityFormset = modelformset_factory(Liability, form=LiabilityForm, extra=1)

    if request.method == 'POST':
        asset_formset = AssetFormset(request.POST, prefix='assets')
        liability_formset = LiabilityFormset(request.POST, prefix='liabilities')
        if asset_formset.is_valid() and liability_formset.is_valid():
            asset_formset.save()
            liability_formset.save()
            # Do something, like redirecting to a new URL
        return redirect('complete_application')
           
    else:
        asset_formset = AssetFormset(queryset=Asset.objects.none(), prefix='assets')
        liability_formset = LiabilityFormset(queryset=Liability.objects.none(), prefix='liabilities')

    return render(request, 'section_12.html', {
        'asset_formset': asset_formset,
        'liability_formset': liability_formset,
    })
    

def company_information_view(request):
    if request.method == 'POST':
        form = CompanyInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_2')  # Replace 'success_url' with the URL name where you want to redirect after the form is saved.
    else:
        form = CompanyInformationForm()

    return render(request, 'section_1.html', {'form': form})


def managing_director_view(request):
    if request.method == 'POST':
        form = ManagingDirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_3')  # Replace 'next_section' with your next section's view name.
    else:
        form = ManagingDirectorForm()

    return render(request, 'section_2.html', {'form': form})

def off_taker_details_view(request):
    if request.method == 'POST':
        form = OffTakerDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_4')  # Replace with your next section's view name.
    else:
        form = OffTakerDetailsForm()

    return render(request, 'section_3.html', {'form': form})


def contract_information_view(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_5')  # Replace with your next section's view name.
    else:
        form = ContractForm()

    return render(request, 'section_4.html', {'form': form})

def invoice_information_view(request):
    if request.method == 'POST':
        form = InvoiceInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('section_6')  # Replace with the next section's view name.
    else:
        form = InvoiceInformationForm()

    return render(request, 'section_5.html', {'form': form})

@login_required(login_url='login')
def section0(request):
    return render(request, "section_0.html")

@login_required(login_url='login')
def section1(request):
    return render(request, "section_1.html")

@login_required(login_url='login')
def section2(request):
    return render(request, "section_2.html")

def section3(request):
    return render(request, "section_3.html")

def section4(request):
    return render(request, "section_4.html")

def section5(request):
    return render(request, "section_5.html")

def section6(request):
    return render(request, "section_6.html")

def section7(request):
    return render(request, "section_7.html")

def section8(request):
    return render(request, "section_8.html")

def section9(request):
    return render(request, "section_9.html")

def section10(request):
    return render(request, "section_10.html")

def section11(request):
    return render(request, "section_11.html")

def section12(request):
    return render(request, "section_12.html")

def section13(request):
    return render(request, "section_13.html")
