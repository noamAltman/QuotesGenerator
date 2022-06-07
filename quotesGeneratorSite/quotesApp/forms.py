from django import forms
from .models import Quote
from django.forms import ModelForm

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'
