from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from blog.models import BlogPage, BlogPost
import re

from core.functions import *

def html_replace(text):
    t = re.sub(r'<[^>]*>', r' ', str(text)).split()
    return ' '.join(t).lower()

def get_tags(tags):
    return [ { 'url': tag.url, 'name': tag.name } for tag in tags ]


def find_items(search_results, page, query):
    model = page.specific.content_type.model
    if model in ['blogindex', 'blogpage', 'blogpost'] and page.title.lower().find(query) > -1:
        search_results.append(page)
    else:
        body = None
        if model == 'blogindex':
            body = html_replace(page.blogindex.body)
        elif model == 'blogpage':
            body = html_replace(page.blogpage.body)
        elif model == 'blogpost':
            body = html_replace(page.blogpost.body)

        if body and body.find(query) > -1:
            search_results.append(page)
    return search_results


def search(request):
    #print(request.user.is_authenticated, request.user.is_superuser)
    method = request.GET.get('method', None)
    query = request.GET.get('query', '').strip().lower()
    
    search_results = []

    # Tag Search    
    if method == 'tag':
        if query:
            blog_pages = live_in_menu(BlogPage.objects).filter(tags__name=query)
            for page in blog_pages:
                types, groups = get_page_restrictions(page)
                search_results = add_menu(request, get_user_groups(request), search_results, page, types, groups)
            
            blog_posts = live_in_menu(BlogPost.objects).filter(tags__name=query)
            for post in blog_posts:
                types, groups = get_page_restrictions(post)
                search_results = add_menu(request, get_user_groups(request), search_results, post, types, groups)
    else:
        # Search
        if query:
            menu = make_menu(request, get_user_groups(request))
            for index in menu:
                search_results = find_items(search_results, index, query)
                for pg in index.children:
                    search_results = find_items(search_results, pg, query)
                    for post in page.children:
                        search_results = find_items(search_results, post, query)

    total_results = len(search_results)
    
    page = request.GET.get('page', 1)

    # Pagination
    paginator = Paginator(search_results, 20)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    for item in results:
        if item.depth == 3:
            item.badge = item
        elif item.depth == 4:
            item.badge = item.get_parent()
        elif item.depth == 5:
            item.badge = item.get_parent().get_parent()

        model = item.specific.content_type.model
        if model == 'blogpage':
            item.tags = get_tags(item.specific.blogpage.get_tags)
        elif model == 'blogpost':
            item.tags = get_tags(item.specific.blogpost.get_tags)

    return TemplateResponse(request, 'search/search.html', {
        'home_page': Page.objects.get(title=settings.WAGTAIL_SITE_NAME),
        'method': method,
        'query': query,
        'total_results': total_results,
        'results': results
    })
