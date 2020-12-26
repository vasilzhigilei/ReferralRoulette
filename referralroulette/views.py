from django.shortcuts import render
from django.http import HttpResponse
from .models import ServiceModel, ReferralModel
import random
from datetime import datetime
random.seed(datetime.now())

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

def generate_referral(request, service):
    links = ReferralModel.objects.filter(service=service)
    if len(links) == 0:
        return HttpResponse("No referral links")
    else:
        i = random.randint(0,len(links))
        return HttpResponse(links[i])