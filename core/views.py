from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache
from django.core.exceptions import SuspiciousOperation


def get_data(meta, field):
    data = settings.SHIB_ATTR_MAP[field]
    if data in meta:
        return meta[data]
    return None


@method_decorator([never_cache], name='dispatch')
class Index(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        full_name = get_data(request.META, 'full_name')
        last_name = get_data(request.META, 'last_name')
        email = get_data(request.META, 'email')
        username = get_data(request.META, 'username')

        if not username:
            raise SuspiciousOperation
        
        first_name = 'Firstname'
        if full_name:
            first_name = full_name.split(last_name)[0].strip()

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