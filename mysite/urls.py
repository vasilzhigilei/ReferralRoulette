"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from referralroulette import views
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new
from django.views.static import serve
from django.conf.urls import url
from django.views.generic import RedirectView

handler404 = 'referralroulette.views.custom_page_not_found_view'
handler500 = 'referralroulette.views.custom_error_view'

urlpatterns = [
    path('', views.index, name='index'),
    path('for/', RedirectView.as_view(url='/')), # empty for/ should redirect to index.html
    path('for/<slug:slug>', views.for_service, name='for_service'),
    path('browse', views.browse, name='browse'),
    path('categories', views.categories, name='categories'),
    path('categories/<slug:slug>', views.categories_tag, name='categories_tag'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
    path('policies/cookie', views.cookiepolicy, name='cookiepolicy'),
    path('policies/privacy', views.privacypolicy, name='privacypolicy'),
    path('profile', views.profile, name='profile'),
    path('redirect/<str:slug>', views.redirect, name='redirect'),
    path('api/generatereferral/<str:slug>', views.generate_referral, name='generate_referral'),
    path('api/addreferral', views.add_referral, name='add_referral'),
    path('api/deletereferral/<str:slug>', views.delete_referral, name='delete_referral'),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
