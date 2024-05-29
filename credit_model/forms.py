from ast import Pass
from pyexpat import model
from django import forms
from .models import  Credit_Model_Input



class Credit_Model_Input_Form(forms.ModelForm):
    class Meta:
        model = Credit_Model_Input
        fields = '__all__'