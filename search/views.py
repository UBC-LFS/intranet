from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.models import Query
from human_resources import models
from communications import models
import re

def html_replace(text):
    t = re.sub(r'<[^>]*>', r' ', str(text)).split()
    return ' '.join(t).lower()

def find_page(page, query, results):
    if page.title.lower().find(query) > -1:
        results.append(page)
        return results

    body = None
    if page.specific.content_type.model == 'aboutpage':
        body = html_replace(page.aboutpage.body)
    elif page.specific.content_type.model == 'communicationpage':
        body = html_replace(page.communicationpage.body)
    elif page.specific.content_type.model == 'facultyresourcepage':
        body = html_replace(page.facultyresourcepage.body)
    elif page.specific.content_type.model == 'financepage':
        body = html_replace(page.financepage.body)
    elif page.specific.content_type.model == 'humanresourcepage':
        body = html_replace(page.humanresourcepage.body)
    elif page.specific.content_type.model == 'newtolfspage':
        body = html_replace(page.newtolfspage.body)
    elif page.specific.content_type.model == 'operationpage':
        body = html_replace(page.operationpage.body)
    elif page.specific.content_type.model == 'policypage':
        body = html_replace(page.policypage.body)

    if body.find(query) > -1:
        results.append(page)
    return results


def get_tags(tags):
    return [ { 'url': tag.url, 'name': tag.name } for tag in tags ]

def search(request):
    search_query = request.GET.get('query', '').strip().lower()
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = []
        pages = Page.objects.live()
        for p in pages:
            if p.depth == 4:
                search_results = find_page(p, search_query, search_results)

        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    total_results = len(search_results)

    # Pagination
    paginator = Paginator(search_results, 20)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    for item in search_results:
        badge = None
        tags = []

        if item.specific.content_type.model == 'aboutpage':
            badge = 'About'
            tags = get_tags(item.specific.aboutpage.get_tags)
        elif item.specific.content_type.model == 'communicationpage':
            badge = 'Communications'
            tags = get_tags(item.specific.communicationpage.get_tags)
        elif item.specific.content_type.model == 'facultyresourcepage':
            badge = 'Faculty Resources'
            tags = get_tags(item.specific.financepage.get_tags)
        elif item.specific.content_type.model == 'financepage':
            badge = 'Finance'
            tags = get_tags(item.specific.financepage.get_tags)
        elif item.specific.content_type.model == 'humanresourcepage':
            badge = 'Human Resources'
            tags = get_tags(item.specific.humanresourcepage.get_tags)
        elif item.specific.content_type.model == 'newtolfspage':
            badge = 'New to LFS'
            tags = get_tags(item.specific.newtolfspage.get_tags)
        elif item.specific.content_type.model == 'operationpage':
            badge = 'Operations'
            tags = get_tags(item.specific.operationpage.get_tags)
        elif item.specific.content_type.model == 'policypage':
            badge = 'Policies'
            tags = get_tags(item.specific.policypage.get_tags)

        item.badge = badge
        item.tags = tags

    return TemplateResponse(request, 'search/search.html', {
            'search_query': search_query,
            'search_results': search_results,
            'total_results': total_results
        },
    )
