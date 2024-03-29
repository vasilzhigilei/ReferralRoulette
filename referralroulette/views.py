from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from .models import ServiceModel, ReferralModel
from .forms import ProfileForm, ReferralForm, ContactForm
from taggit.models import Tag
from django.db.models import Count
import random
import json
import urllib
from datetime import datetime
from django.http import Http404
import json
random.seed(datetime.now())

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'top_services': ServiceModel.objects.order_by('-clicks')[0:20],
        'featured': featured,
    }
    return render(request, "index.html", context)

def for_service(request, slug):
    try:
        for_service = ServiceModel.objects.get(slug=slug)
    except ServiceModel.DoesNotExist:
        raise Http404
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
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    
    pagetitle = for_service.name + ' Referral Link ' + for_service.description
    if for_service.code:
        pagetitle = for_service.name + ' Referral Code ' + for_service.description
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'for_service': for_service,
        'related': for_service.tags.similar_objects()[0:7],
        'link': link,
        'users': len(links),
        'featured': featured,
        'pagetitle': pagetitle,
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
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
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
        data = {
            'link': "No referral links",
            'users': 0
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        i = random.randint(0,len(links)-1)
        link_object = links[i]
        link_object.clicks += 1
        link_object.save()
        service_object = ServiceModel.objects.get(slug=slug)
        service_object.clicks += 1
        service_object.save()
        data = {
            'link': link_object.link,
            'users': len(links)
        }
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

def redirect(request, slug):
    try:
        service = ServiceModel.objects.get(slug=slug)
        return HttpResponseRedirect(service.default_link)
    except ServiceModel.DoesNotExist:
        return HttpResponseRedirect("/")

@login_required(login_url='/accounts/google/login/')
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    user_links = ReferralModel.objects.filter(email=request.user.email)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully updated profile!")
        return HttpResponseRedirect(reverse('profile'))
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'profileform': form,
        'referralform': ReferralForm(),
        'user_links': user_links,
        'featured': featured,
        'pagetitle': 'My Profile',
    }
    return render(request, "profile.html", context)

def add_referral(request):
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
            service = ServiceModel.objects.get(slug=referral.slug)
            prefix = service.prefix
            if(len(referral.link) < len(prefix)):
                messages.error(request, "Link does not match prefix: " + prefix)
            elif (prefix != referral.link[0:len(prefix)]):
                messages.error(request, "Link does not match prefix: " + prefix)
            else:
                if service.code:
                    referral.save()
                    messages.success(request, "Successfully added code!")
                else:
                    referral.save()
                    messages.success(request, "Successfully added link!")    
        return HttpResponseRedirect(reverse('profile'))
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'profileform': ProfileForm(),
        'referralform': form,
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
    categories = {"finance": "Finance",
                "cryptocurrency": "Cryptocurrency",
                "travel": "Travel",
                "food": "Food",
                "retail": "Retail",
                "rewards": "Rewards",
    }
    top_of_categories = {}
    for category_key in categories: # category_key is slug
        top_of_categories[category_key] = ServiceModel.objects.filter(tags__name__in=[category_key]).order_by('-clicks')[0:6]

    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
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
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }
    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages
        'category_services': ServiceModel.objects.filter(tags__name__in=[slug]),
        'featured': featured,
        'category': slug.title(),
        'pagetitle': slug.title(),
    }
    return render(request, "categories_tag.html", context)

def browse(request):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
        'food': ServiceModel.objects.filter(tags__name__in=['food']).order_by('-clicks')[0:5],
    }

    context = {
        'services': ServiceModel.objects.all(), # for the search bar, all pages. For "Browse" page also used for loop
        'featured': featured,
        'pagetitle': 'Browse',
    }
    return render(request, "browse.html", context)

def faq(request):
    featured = {
        'finance': ServiceModel.objects.filter(tags__name__in=['finance']).order_by('-clicks')[0:5],
        'cryptocurrency': ServiceModel.objects.filter(tags__name__in=['cryptocurrency']).order_by('-clicks')[0:5],
        'travel': ServiceModel.objects.filter(tags__name__in=['travel']).order_by('-clicks')[0:5],
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