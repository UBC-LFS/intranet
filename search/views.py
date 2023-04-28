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
    if page.specific.content_type.model == 'communicationpage':
        body = html_replace(page.communicationpage.body)
    elif page.specific.content_type.model == 'financepage':
        body = html_replace(page.financepage.body)
    elif page.specific.content_type.model == 'humanresourcepage':
        body = html_replace(page.humanresourcepage.body)
    elif page.specific.content_type.model == 'learningcentrepage':
        body = html_replace(page.learningcentrepage.body)
    elif page.specific.content_type.model == 'operationpage':
        body = html_replace(page.operationpage.body)

    if body.find(query) > -1:
        results.append(page)
    return results


def search(request):
    search_query = request.GET.get('query', '').strip().lower()
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = []
        pages = Page.objects.live()
        for p in pages:
            if p.depth == 4:
                print(p.specific, p.specific.content_type.model)
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

    return TemplateResponse(request, 'search/search.html', {
            'search_query': search_query,
            'search_results': search_results,
            'total_results': total_results
        },
    )
