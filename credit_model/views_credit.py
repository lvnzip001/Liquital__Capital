import http
from traceback import format_exception_only
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import Credit_Model_Input_Form
from .models import Credit_Model_Input
import os
from django.conf import settings
from mysite.settings import MEDIA_ROOT


import pandas as pd
import numpy as np
import json
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors

from .sme_rating.data import overallCreditScore, run_all_credit_func, convert_to_df
from .sme_rating.convertTOCSV_zl import add_to_csv_file
from .sme_rating.company_data import (
    convertToDataFrame,
    getCompanyData,
    getcompanybyname,
    getallcompanynames,
)

from .sme_rating.ratings_data import getRatingsData, getScoresData, getFactors, getRatingsByDefaultProbability
from .sme_rating.variable_weighting_data import getWeightingData

# Define the path to the sme_rating folder
SME_RATING_FOLDER = os.path.join(settings.BASE_DIR, "credit_model/sme_rating")

def home(request):
    return render(request, "home.html")


def about_us(request):

    return render(request, "about_us.html")


def data_pdf(request):
    # Create bytestream buffer

    # return FileResponse(buf, as_attachment=True, filename= 'Credit_rating')
    return HttpResponse("work")


def registered(request):
    # first function to get the list of files in the dummy data
    filename = SME_RATING_FOLDER + "/dummy_companies.txt"
    entity_names = getallcompanynames(filename)
    # breakpoint()
    for i in entity_names:
        print(i)
    return render(request, "registered.html", entity_names)


def registered_data_input(request, company=None):
    # first function to get the list of files in the dummy data
    company_data = SME_RATING_FOLDER + "/dummy_companies.txt"
    ratings_data = SME_RATING_FOLDER + "/ratings.txt"
    weightings_data = SME_RATING_FOLDER + "/variable_weightings.txt"
    score_data = SME_RATING_FOLDER + "/scores.txt"
    pd_rating_tbl = SME_RATING_FOLDER + '\Demo sme_rating Model.xlsx'
    
    companies = [getcompanybyname(company, company_data)]
   

    company_info = dict(list(companies[0].items())[:3])
    for k in company_info.keys():
        # k_new = k
        k_new = k.replace(" ", "_")
        company_info[k_new] = company_info.pop(k)

    company_info = convert_to_df(company_info)
    
    credit_rating_tbl = run_all_credit_func(companies[0], 
                                            ratings_data, 
                                            weightings_data,
                                            score_data)

    credit_score_summary = convert_to_df(overallCreditScore(company, 
                                                            companies[0],
                                                            company_data,
                                                            weightings_data,
                                                            score_data, 
                                                            ratings_data,
                                                            pd_rating_tbl))

    credit_rating_tbl_json = credit_rating_tbl.reset_index().to_json(orient="records")

    credit_score_summary_json = credit_score_summary.reset_index().to_json(
        orient="records"
    )
    company_info_json = company_info.reset_index().to_json(orient="records")
    # company_info =
    data = []
    data = json.loads(credit_rating_tbl_json)
    data.append(json.loads(company_info_json))
    data.append(json.loads(credit_score_summary_json))

    context = {"d": data[:-2], "d1": data[-1], "d2": data[-2]}

    print(context["d1"])

    return render(request, "credit_rating_tbl.html", context)
    # return HttpResponse("It kinda works for " + str(company))


def data_input(request):
    
     # first function to get the list of files in the dummy data
    company_data = SME_RATING_FOLDER + "/dummy_companies.txt"
    ratings_data = SME_RATING_FOLDER + "/ratings.txt"
    weightings_data = SME_RATING_FOLDER + "/variable_weightings.txt"
    score_data = SME_RATING_FOLDER + "/scores.txt"
    pd_rating_tbl = SME_RATING_FOLDER + '\Demo sme_rating Model.xlsx'

    if request.method == "POST":
        form = Credit_Model_Input_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            last_object = Credit_Model_Input.objects.all().last()
            last_object_location = MEDIA_ROOT + f"{last_object.file}"
            add_to_csv_file(filename=company_data, excel_input_file=last_object_location)
            
            company_name = getCompanyData(company_data)[0]["Entity Name"]
            companies = [getcompanybyname(company_name)]

            company_info = dict(list(companies[0].items())[:3])
            for k in company_info.keys():
                # k_new = k
                k_new = k.replace(" ", "_")
                company_info[k_new] = company_info.pop(k)

            company_info = convert_to_df(company_info)
            credit_rating_tbl = run_all_credit_func(companies[0])
            credit_score_summary = convert_to_df(
                overallCreditScore(company_name, companies[0])
            )

            # credit_rating_tbl = df.to_html()
            #
            # parsing the DataFrame in json format.
            credit_rating_tbl_json = credit_rating_tbl.reset_index().to_json(
                orient="records"
            )
            credit_score_summary_json = credit_score_summary.reset_index().to_json(
                orient="records"
            )
            company_info_json = company_info.reset_index().to_json(orient="records")
            # company_info =
            data = []
            data = json.loads(credit_rating_tbl_json)
            data.append(json.loads(company_info_json))
            data.append(json.loads(credit_score_summary_json))

            context = {"d": data[:-2], "d1": data[-1], "d2": data[-2]}
            
            print(context["d1"])
           

        #breakpoint()
        return render(request, "credit_rating_tbl.html", context)

    else:
        #
        form = Credit_Model_Input_Form()

    return render(request, "data_input.html", {"form": form})


def test(request):

    return HttpResponse("What the Fuck")


def data_pdf(request, Entity_Name):
    # Create bytestream buffer
    buf = io.BytesIO()

    # create CAnvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    c.setTitle("Credit Model")

    # create text object
    textob = c.beginText()
    # textob.setTextOrigin(inch,inch)

    # Add lines of test
    companies = [getcompanybyname(Entity_Name)]
    credit_rating_tbl = run_all_credit_func(companies[0])

    credit_score_summary = convert_to_df(overallCreditScore(Entity_Name, companies[0]))

    company_info = dict(list(companies[0].items())[:3])
    company_info = convert_to_df(company_info)

    lines = ["This is  line 1" "This is  line 2" "This is  line 3"]

    # coordinate Numbers are the coordinates
    c.drawString(30, 30, f"Credit Model for {Entity_Name}")
    c.line(30, 40, 580, 40)
    # For Large amounts of text
    textob = c.beginText(30, 70)
    textob.setFont("Helvetica", 12)
    textob.setFillColor(colors.black)

    textlines = [
                f"This credit model was generated for {Entity_Name}. A credit scoring model is a mathematical model ",
                " used to estimate the probability of default, which is the probability, that customers may trigger a credit",
                " event (i.e. bankruptcy, obligation default, failure to pay,and cross-default events). In a credit scoring",
                " model, the probability of default is normally presented in the form of a credit score. The higher score ",
                 "refers to a lower probability of default.",
                 "",
                 f"This report was generate for {company_info[['Funding Type']].iloc[0,0]}. {Entity_Name} credit_score summary: ",
                 "",
                 f"- Stand Alone Credit Score: {float(credit_score_summary['stand_alone_credit_score'])}",
                 f"- Overall Credit Score: {float(credit_score_summary['overall_credit_score'])}",
                 f"- Probability Of Default: {float(credit_score_summary['probability_of_default'])}",
                 f"- Credit rating: {credit_score_summary[['credit_rating']].iloc[0,0]}",
                 "",
                 "",
                 "",
                 "The below table contains investment Credit rating grading and group: "



                ]
    # So for the text it seems we always need some for loop
    
    for line in textlines:   
        textob.textLine(line)
        
        print(line)

    c.showPage
    c.drawText(textob)
    #photo_location = MEDIA_ROOT + "/Credit-rating.png"
    #print(photo_location)
    c.line(30, 255, 580, 255)
    #c.drawInlineImage("Picture2.jpg",80,305)
    
    c.save()
    buf.seek(0)
   
    return FileResponse(buf, as_attachment=True, filename="Credit_rating.pdf")
