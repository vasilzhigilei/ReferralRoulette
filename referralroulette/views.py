from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import ServiceModel, ReferralModel, CategoryModel
from .forms import ProfileForm, ReferralForm
import random
from datetime import datetime
random.seed(datetime.now())

def index(request):
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'top_services': ServiceModel.objects.order_by('-clicks')[0:20],
        'categories': CategoryModel.objects.all(),
    }
    return render(request, "index.html", context)

def for_service(request, slug):
    links = ReferralModel.objects.filter(slug=slug)
    link = ""
    if len(links) == 0:
        link = "No links error"
    else:
        i = random.randint(0,len(links)-1)
        link_object = links[i]
        link_object.clicks += 1
        link_object.save()
        service_object = ServiceModel.objects.get(slug=slug)
        service_object.clicks += 1
        service_object.save()
        link = link_object.link
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'for_service': ServiceModel.objects.get(slug=slug),
        'link': link,
        'users': len(links)
    }
    # should have a try except here of ServiceModel.DoesNotExist
    return render(request, "for.html", context)

def generate_referral(request, slug):
    links = ReferralModel.objects.filter(slug=slug)
    if len(links) == 0:
        return HttpResponse("No referral links")
    else:
        i = random.randint(0,len(links)-1)
        return HttpResponse(links[i].link)

@login_required(login_url='/accounts/google/login/')
def profile(request):
    form = ReferralForm(request.POST or None)

    user_links = ReferralModel.objects.filter(email=request.user.email)
    if form.is_valid():
        referral = form.save(commit=False)
        referral.email = request.user.email
        referral.slug = slugify(request.POST.get('service'))
        num_results = ReferralModel.objects.filter(email=request.user.email, slug=referral.slug).count()
        if num_results != 0:
            messages.error(request, "You've already added this app's link.")
        else:
            referral.save()
            messages.success(request, "Successfully added link!")
        return HttpResponseRedirect(reverse('profile'))
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'form': form,
        'user_links': user_links,
    }
    return render(request, "profile.html", context)

def delete_referral(request, slug):
    if request.method == 'POST':
        ReferralModel.objects.filter(email=request.user.email, slug=slug).delete()
        return HttpResponseRedirect(request.path)
    return HttpResponseRedirect("/profile")


def categories(request):
    categories = CategoryModel.objects.all()
    top_of_categories = {}
    for category in categories:
        top_of_categories[category] = ServiceModel.objects.filter(tags__name__in=[category.slug]).order_by('-clicks')[0:8]
    print(top_of_categories)
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'categories': categories,
        'top_of_categories': top_of_categories,
    }
    return render(request, "categories.html", context)

def faq(request):
    return render(request, "faq.html")