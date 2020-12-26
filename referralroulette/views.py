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
    links = ReferralModel.objects.filter(service=slug)
    link = ""
    if len(links) == 0:
        link = "No links error"
    else:
        i = random.randint(0,len(links))
        link = links[i]
    context = {
        'services': ServiceModel.objects.all(),
        'for_service': ServiceModel.objects.get(slug=slug),
        'link': link,
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