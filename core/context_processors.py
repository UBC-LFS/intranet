from django.conf import settings
from wagtail.models import Page
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from core.functions import *

def navbar_menu(request):
    return {
        'navbar_menu': make_menu(request, get_user_groups(request))
    }


def current_page(request):
    full_path = request.get_full_path()
    if full_path == '/':
        full_path = '/' + slugify(settings.WAGTAIL_SITE_NAME) + '/'

    page = Page.objects.filter(url_path=full_path)
    return {
        'current_page':  page.first() if page.exists() else None
    }