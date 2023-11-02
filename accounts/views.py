from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as DjangoLogin

from .forms import LocalLoginForm


def local_login(request):
    if request.method == 'POST':
        form = LocalLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                perms = list(user.get_group_permissions())
                if user.is_superuser or 'wagtailadmin.access_admin' in perms:
                    DjangoLogin(request, user)
                    return HttpResponseRedirect(settings.ADMIN_PORTAL_HOME_PAGE)
            else:
                messages.error(request, 'Error! No user found.')
        else:
            messages.error('Error! Form is not valid.')

        return HttpResponseRedirect('/')

    return render(request, 'accounts/local_login.html', {
        'form': LocalLoginForm()
    })
