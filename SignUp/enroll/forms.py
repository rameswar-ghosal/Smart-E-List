from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from enroll.models import Selectoptions,Scheduled
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm

class Authenticate(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'iamclass','placeholder':'Username ...'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'iamclass','placeholder':'Password ...'}))

class Setpassword(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'iamclass','placeholder':'New Password ...'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'iamclass','placeholder':'Confirm Password ...'}))


class SignUpForm(UserCreationForm):
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Pass.','class':'sel1'}))
  password2 = forms.CharField(label="Confirm Password (again)",
  widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Pass.','class':'sel1'}))

  class Meta:
    model = User
    fields = ['username','first_name','last_name','email']
    labels = {'email':'Email'}
    widgets ={
        'username':  forms.TextInput(attrs={'placeholder':'Enter Username ','class':'sel1'}),
        'first_name':forms.TextInput(attrs={'required':'true','placeholder':'Enter Firstname  ','class':'sel1'}),
        'last_name': forms.TextInput(attrs={'required':'true','placeholder': 'Enter Lastname  ','class':'sel1'}),
        'email':     forms.EmailInput(attrs={'required':'true','placeholder': 'Enter Email  ','class':'sel1'}),
    }

class select(forms.ModelForm):
  class Meta:
     model = Selectoptions
     fields = ['city_name','phone_no']
     widgets = {
         'city_name': forms.TextInput(attrs={'placeholder': 'Enter Your City ','class':'sel1'}),
         'phone_no': forms.TextInput(attrs={'placeholder':'Enter Your Phone No ','class':'sel1'}),
        }

class uniquekey(forms.ModelForm):
    class Meta:
        model = Selectoptions
        fields=['unique_key']

        widgets = {
            'unique_key': forms.PasswordInput(attrs={'placeholder': 'UniqueKey of your choice', 'class': 'ukey','size':'20'}),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
'''
class DInput(forms.DateTimeInput):
    input_type = 'datetime-local'
'''

class your_list(forms.ModelForm):
    class Meta:

         model = Scheduled
         fields=['schedule_items','schedule_date','schedule_time']

         widgets = {
                      'schedule_date':DateInput(attrs={'class':'SI'}),'schedule_time':TimeInput(attrs={'class':'SI'}),
             'schedule_items':forms.Textarea(attrs={'rows':3,'cols':17,'class':'SI','placeholder':'To Schedule Something, Write Here :)'}),

         }
class Sendingmail(forms.Form):
    Sender_Email_id = forms.EmailField( widget=forms.EmailInput(
        attrs={'placeholder': 'Enter Sender Email Here ...','size':'18','class':'e'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password Here ...','size':'18','class':'e'})
                               )
    Receiver_Email_id = forms.EmailField( widget=forms.EmailInput(
        attrs={ 'placeholder': 'Enter Receiver Email Here ...','size':'18','class':'e'}))
    Subject = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Write Subject Here ...', 'rows': 3, 'cols': 22,'class':'e'}), max_length=100
                              )
    Body = forms.CharField(
        widget=forms.Textarea(attrs={ 'placeholder': 'Write Body Here ...', 'rows': 5, 'cols': 22,'class':'e'}),
        max_length=100)



class searchquery(forms.Form):

    place=forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'placeholder': 'Place ... Eg. Arsande, a place of Ranchi City', 'size':25,'class':'search'}),
        max_length=50)
    search=forms.CharField(widget=forms.TextInput(attrs={'required': 'true', 'placeholder': ' Search Items Place / Just Place','class':'search'}),
        max_length=50)
