from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.models import Query
from blog.models import BlogIndex, BlogPage, BlogPost

import re

def html_replace(text):
    t = re.sub(r'<[^>]*>', r' ', str(text)).split()
    return ' '.join(t).lower()

def get_tags(tags):
    return [ { 'url': tag.url, 'name': tag.name } for tag in tags ]

def search(request):
    method = request.GET.get('method', None)
    query = request.GET.get('query', '').strip().lower()
    
    pages = Page.objects.live()
    
    search_results = []

    # Tag Search    
    if method == 'tag':
        if query:
            blog_pages = BlogPage.objects.filter(tags__name=query)
            blog_posts = BlogPost.objects.filter(tags__name=query)
            search_results = blog_pages.union(blog_posts)
    else:
        # Search
        if query:
            for page in pages:
                if page.depth >= 3:
                    if page.title.lower().find(query) > -1:
                        search_results.append(page)
                    else:
                        model = page.specific.content_type.model

                        body = None
                        if model == 'blogindex':
                            body = html_replace(page.blogindex.body)
                        elif model == 'blogpage':
                            body = html_replace(page.blogpage.body)
                        elif model == 'blogpost':
                            body = html_replace(page.blogpost.body)
                        
                        if body.find(query) > -1:
                            search_results.append(page)

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
