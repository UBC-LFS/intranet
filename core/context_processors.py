from django.conf import settings
from wagtail.models import Page
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from core.functions import *

def can_access_wagtail_admin(request):
    return {
        'can_access_wagtail_admin': request.user.has_perm('wagtailadmin.access_admin')
    }

def navbar_menu(request):
    return {
        'navbar_menu': make_menu(request, get_user_groups(request))
    }

def current_page(request):
    full_path = request.get_full_path()
    if full_path == '/':
        full_path = make_slug()

    page = Page.objects.filter(url_path=full_path)
    return {
        'current_page':  page.first() if page.exists() else None
    }

def site_name_slug(request):
    return {
        'site_name_slug': make_slug()
    }


# Helper functions

def make_slug():
    return '/' + slugify(settings.WAGTAIL_SITE_NAME) + '/'
    