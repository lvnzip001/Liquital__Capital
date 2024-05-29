from distutils.command.upload import upload
from pickle import TRUE
from django.db import models
from django.dispatch import receiver
import os
#from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
import hashlib
import random

# Create your models here.
#@deconstructible


class Credit_Model_Input(models.Model):
    user = models.CharField(max_length=100)
    file = models.FileField(upload_to='model_input/',null=False,blank=False)

