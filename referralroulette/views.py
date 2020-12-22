from django.shortcuts import render
from django.http import HttpResponse
from .models import ServiceModel, ReferralModel

def index(request):
    context = {
        'services': ServiceModel.objects.all(),
    }
    return render(request, "index.html", context)