from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import ServiceModel, ReferralModel, CategoryModel
from .forms import ProfileForm, ReferralForm, ContactForm
from taggit.models import Tag
from django.db.models import Count
import random
import json
import urllib
from datetime import datetime
random.seed(datetime.now())

def index(request):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'top_services': ServiceModel.objects.order_by('-clicks')[0:20],
        'categories': CategoryModel.objects.all(),
        'featured': featured,
    }
    return render(request, "index.html", context)

def for_service(request, slug):
    links = ReferralModel.objects.filter(slug=slug)
    link = ""
    if len(links) == 0:
        link = "No referral links"
    else:
        i = random.randint(0,len(links)-1)
        link_object = links[i]
        link_object.clicks += 1
        link_object.save()
        service_object = ServiceModel.objects.get(slug=slug)
        service_object.clicks += 1
        service_object.save()
        link = link_object.link
    
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    for_service = ServiceModel.objects.get(slug=slug)
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'for_service': for_service,
        'related': for_service.tags.similar_objects()[0:7],
        'link': link,
        'users': len(links),
        'featured': featured,
        'pagetitle': for_service.name,
        'categories': CategoryModel.objects.all(),
    }
    # should have a try except here of ServiceModel.DoesNotExist
    return render(request, "for.html", context)

@login_required(login_url='/accounts/google/login/')
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            payload = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(payload).encode()
            req = urllib.request.Request(url, data=data)

            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            
            if (not result['success']):  # make sure action matches the one from your template
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            else:
                contact = form.save(commit=False)
                contact.from_email = request.user.email
                contact.save()
                messages.success(request, "Successfully sent!")
                return HttpResponseRedirect(reverse('contact'))
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'featured': featured,
        'pagetitle': 'Contact',
        'site_key': settings.RECAPTCHA_SITE_KEY,
        'form': form,
    }
    return render(request, "contact.html", context)

def generate_referral(request, slug):
    links = ReferralModel.objects.filter(slug=slug)
    if len(links) == 0:
        return HttpResponse("No referral links")
    else:
        i = random.randint(0,len(links)-1)
        link_object = links[i]
        link_object.clicks += 1
        link_object.save()
        service_object = ServiceModel.objects.get(slug=slug)
        service_object.clicks += 1
        service_object.save()
        link = link_object.link
        return HttpResponse(link)

def redirect(request, slug):
    try:
        service = ServiceModel.objects.get(slug=slug)
        return HttpResponseRedirect(service.default_link)
    except ServiceModel.DoesNotExist:
        return HttpResponseRedirect("/") # need some error page, and implement 404 management

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
            prefix = ServiceModel.objects.get(slug=referral.slug).prefix
            if(len(referral.link) < len(prefix)):
                messages.error(request, "Link does not match prefix: " + prefix)
            elif (prefix != referral.link[0:len(prefix)]):
                messages.error(request, "Link does not match prefix: " + prefix)
            else:
                referral.save()
                messages.success(request, "Successfully added link!")
        return HttpResponseRedirect(reverse('profile'))
    
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'form': form,
        'user_links': user_links,
        'featured': featured,
        'pagetitle': 'My Profile',
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
    
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }

    queryset = Tag.objects.all()
    queryset2 = queryset.annotate(num_times=Count('taggit_taggeditem_items'))
    words = []
    for tag in queryset2:
        words.append([tag.name, tag.num_times])
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'categories': categories,
        'top_of_categories': top_of_categories,
        'featured': featured,
        'pagetitle': 'Categories',
        'words': words
    }
    return render(request, "categories.html", context)

def categories_tag(request, slug):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.filter(tags__name__in=[slug]),
        'categories': CategoryModel.objects.all(),
        'featured': featured,
        'category': slug.title(),
        'pagetitle': slug.title(),
    }
    return render(request, "categories_tag.html", context)

def faq(request):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'hotels': ServiceModel.objects.filter(tags__name__in=['hotels']).order_by('-clicks')[0:5],
        'transport': ServiceModel.objects.filter(tags__name__in=['transport']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'featured': featured,
        'pagetitle': 'FAQ',
    }
    return render(request, "faq.html", context)

def privacypolicy(request):
    return render(request, "privacypolicy.html")

def cookiepolicy(request):
    return render(request, "cookiepolicy.html")

def custom_page_not_found_view(request, exception):
    response = render(request, "errors/404.html")
    response.status_code = 404
    return response

def custom_error_view(request, exception=None):
    response = render(request, "errors/500.html")
    response.status_code = 500
    return response