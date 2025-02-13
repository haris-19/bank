from django import forms

from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name',"Mobile_number","email","aadhaar_card_no","father_name","dob","gender","photo","address",'state']