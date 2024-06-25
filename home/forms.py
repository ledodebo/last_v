from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from .models import CartItem
import datetime
 
from django.forms import ModelForm
from .models import order
class SignUpForm(UserCreationForm):
	
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	class Meta:
		
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'







"""
class order(forms.Form):
    zone = (
        ('c',"القاهرة"),
        ('g',"الجيزة"),
        ('a',"العصيد"),
        ('d',"الدلتا"),
        ('b',"الغردقة-البحر-الاحمر"),
        ('s',"شرم-الشيخ-جنوب سيناء"),
        ('n',"المدن-الجديدة"),
        ('m',"مدينة-بدر"),
        ('x',"اسكندرية"),
        ('xs',"اطراف-الاسكندرية"),
        ('q',"القناة"),
    )
    #iteams = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email =forms.CharField(max_length=250) 
    name = forms.CharField(max_length=250)
    zones = forms.ChoiceField(choices=zone)
    adress=forms.CharField(max_length=250)
    phone=forms.CharField(max_length=250)
    status=forms.BooleanField(initial=False)
    date=forms.DateField(initial=datetime.datetime.today)
    quantity=forms.IntegerField(initial=1)
  
    

    def __str__(self) :
        return self.adress
    
"""

class order(ModelForm):


    class Meta:

        model = order
        fields = ['email','name','zones','adress','phone','phone2']
		



