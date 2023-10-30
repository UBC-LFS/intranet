from django.conf import settings
from wagtail.models import Page

from core.functions import *

def navbar_menu(request):
    return {
        'navbar_menu': make_menu(request, get_user_groups(request))
    }
