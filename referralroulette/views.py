from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import ServiceModel, ReferralModel
from .forms import ProfileForm, ReferralForm
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
        'users': len(links)
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

def profile(request):
    form = ReferralForm(request.POST or None)

    user_links = ReferralModel.objects.filter(email=request.user.email)
    if form.is_valid():
        referral = form.save(commit=False)
        referral.email = request.user.email
        print(request.user.email, request.POST.get('service'))
        print(ReferralModel.objects.filter(email=request.user.email, service=request.POST.get('service')))
        num_results = ReferralModel.objects.filter(email=request.user.email, service=request.POST.get('service')).count()
        print(num_results)
        if num_results != 0:
            messages.error(request, "Referral link already exists.")
        else:    
            referral.save()
            messages.success(request, "Successfully added link!")
        return HttpResponseRedirect(reverse('profile'))
    context = {
        'form': form,
        'user_links': user_links,
    }
    return render(request, "profile.html", context)

def delete_referral(request, service):
    if request.method == 'POST':
        ReferralModel.objects.filter(email=request.user.email, service=service).delete()
        return HttpResponseRedirect(request.path)
    return HttpResponseRedirect("/profile")


def categories(request):
    return render(request, "categories.html")

def faq(request):
    return render(request, "faq.html")