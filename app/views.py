from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import logout

from core.functions import get_home


@method_decorator([never_cache], name='dispatch')
class LandingPage(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'app/landing_page.html', {
            'page': get_home()
        })


@method_decorator([never_cache], name='dispatch')
class Logout(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/Shibboleth.sso/Logout')


def get_data(meta, field):
    data = settings.SHIB_ATTR_MAP[field]
    if data in meta:
        return meta[data]
    return None


@method_decorator([never_cache], name='dispatch')
class Login(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        first_name = get_data(request.META, 'first_name')
        last_name = get_data(request.META, 'last_name')
        email = get_data(request.META, 'email')
        username = get_data(request.META, 'username')

        if not username:
            raise SuspiciousOperation

        # Update user information if it's None
        update_fields = []
        if not request.user.first_name and first_name:
            request.user.first_name = first_name
            update_fields.append('first_name')
        
        if not request.user.last_name and last_name:
            request.user.last_name = last_name
            update_fields.append('last_name')
            
        if not request.user.email and email:
            request.user.email = email
            update_fields.append('email')
        
        if len(update_fields) > 0:
            request.user.save(update_fields=update_fields)        
        
        return HttpResponseRedirect(settings.ADMIN_PORTAL_HOME_PAGE)