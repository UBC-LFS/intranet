from wagtail.models import Page
from django.shortcuts import get_object_or_404

from core.functions import *

def navbar_menu(request):
    return {
        'navbar_menu': make_menu(request, get_user_groups(request))
    }


def current_page(request):
    page = Page.objects.filter(url_path=request.get_full_path())
    return {
        'current_page':  page.first() if page.exists() else None
    }