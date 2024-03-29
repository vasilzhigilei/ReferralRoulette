from django import forms
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ReferralModel, ServiceModel, ContactModel

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_login', 'date_joined')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control forminput'}), 
            'email': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}), 
            'last_login': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}), 
            'date_joined': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}),
        }
        labels = {
            'username': gettext_lazy('Username'),
            'email': gettext_lazy('Email'),
            'last_login': gettext_lazy('Last login'),
            'date_joined': gettext_lazy('Date joined'),
        }
        help_texts = {
            'username': None,
            'email': None,
        }

class ReferralForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=ServiceModel.objects.all(), to_field_name="name", widget=forms.Select(attrs={'class': 'form-control forminput'}))
    class Meta:
        model = ReferralModel
        fields = ('service', 'link')
        widgets = {
            'link': forms.TextInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'link': {'unique': "This referral link already exists in the website."}
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ('subject', 'message')
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control', 'required': 'required'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control', 'required': 'required'})
        }