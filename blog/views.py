import os
import json
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache


@method_decorator([never_cache], name='dispatch')
class Directory(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        users = []

        if not settings.DIRECTORY_PRIVATE or (settings.DIRECTORY_PRIVATE and request.user.is_authenticated):
            users_json = os.path.join(settings.DIRECTORY_PATH, 'users.json')
            if os.path.isdir(settings.DIRECTORY_PATH) and os.path.isfile(users_json):
                with open(users_json, 'r', encoding='utf-8') as f:
                    users = json.loads(f.read())
        else:
            return HttpResponseRedirect('/app/')
        
        return render(request, 'blog/directory.html', {
            'users': sorted(users, key=lambda u: u[ settings.SHIB_ATTR_MAP['last_name'] ])
        })