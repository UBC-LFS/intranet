import os
import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.decorators.cache import never_cache


BASE_URL = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_URL, 'data', 'users.json')

@method_decorator([never_cache], name='dispatch')
class Directory(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        users = []
        if os.path.isfile(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                users = json.loads(f.read())
        else:
            users = get_data()
            
        return render(request, 'blog/directory.html', {
            'users': users
        })


def get_data():
    users = []
    has_next_page = True
    page = 1
    while has_next_page:
        res = requests.get(
            settings.INTRANET_DIRECTORY_API_URL + '&page=' + str(page),
            headers = {
                'x-client-id': settings.INTRANET_DIRECTORY_API_CLIENT_ID, 
                'x-client-secret': settings.INTRANET_DIRECTORY_API_CLIENT_SECRET
            }
        )
        if res.status_code == 200:
            users.extend(res.json()['pageItems'])
            has_next_page = res.json()['hasNextPage']
            page += 1
        else:
            print('Failed to get data via API for some reason.')
            break
    
    if len(users) > 0:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        
    return users