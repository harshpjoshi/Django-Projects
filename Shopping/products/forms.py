from django import forms
from django.forms import ModelForm
from .models import Cart,Order

# simple django forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

# model forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['firstname','lastname','address','zipcode','mobile']
