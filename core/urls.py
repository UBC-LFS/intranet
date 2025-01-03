from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from app import views as app_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', include(wagtailadmin_urls)),
    path('search/', search_views.search, name='search'),
    path('logout/', app_views.Logout.as_view(), name='logout'),
    path('app/', app_views.Login.as_view(), name='login'),
    # path('lfs-intranet/directory/', blog_views.Directory.as_view(), name='directory'),
    path('', app_views.LandingPage.as_view(), name='landing_page')

    #path("documents/", include(wagtaildocs_urls))
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [ 
        path('django-admin/', admin.site.urls)
    ]


if settings.LOCAL_LOGIN:
    urlpatterns += [
        path('accounts/', include('accounts.urls'))
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('lfs-intranet/', include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
