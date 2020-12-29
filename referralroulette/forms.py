from django import forms
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User
from .models import ReferralModel, ServiceModel

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control forminput'}), 
            'email': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}), 
            'first_name': forms.TextInput(attrs={'class': 'form-control forminput'}), 
            'last_name': forms.TextInput(attrs={'class': 'form-control forminput'}), 
            'last_login': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}), 
            'date_joined': forms.TextInput(attrs={'class': 'form-control forminput', 'readonly': 'readonly'}),
        }
        labels = {
            'username': gettext_lazy('Username'),
            'email': gettext_lazy('Email'),
            'first_name': gettext_lazy('First name'),
            'last_name': gettext_lazy('Last name'),
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