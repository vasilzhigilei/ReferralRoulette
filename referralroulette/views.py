from django.shortcuts import render
from django.http import HttpResponse
from .models import ServiceModel, ReferralModel

def index(request):
    context = {
        'services': ServiceModel.objects.all(),
    }
    return render(request, "index.html", context)

def for_service(request, slug):
    context = {
        'services': ServiceModel.objects.all(),
        'for_service': ServiceModel.objects.get(slug=slug),
    }
    # should have a try except here of ServiceModel.DoesNotExist
    return render(request, "for.html", context)