from django.conf import settings
from wagtail.models import Page


def get_user_groups(request):
    return [ group.name for group in request.user.groups.all() ]


def get_page_restrictions(page):
    types = [ res.restriction_type for res in page.get_view_restrictions() ]
    groups = []
    if len(types) > 0:
        for res in page.get_view_restrictions():
            for group in res.groups.all():
                groups.append(group.name)
    return types, groups


def add_menu(request, user_groups, menu, page, types, groups):
    if (len(types) == 0) or (request.user.is_authenticated and request.user.is_superuser):
        menu.append(page)
    else:
        is_group_in = False
        for g in groups:
            if g in user_groups:
                is_group_in = True
                break

        if 'login' in types and request.user.is_authenticated:
            menu.append(page)
        elif 'password' in types and request.user.is_authenticated and request.user.is_superuser:
            menu.append(page)
        elif 'groups' in types and is_group_in == True:
            menu.append(page)
    
    return menu


def get_page_restrictions(page):
    types = [ res.restriction_type for res in page.get_view_restrictions() ]
    groups = []
    if len(types) > 0:
        for res in page.get_view_restrictions():
            for group in res.groups.all():
                groups.append(group.name)
    return types, groups


def add_menu(request, user_groups, menu, page, types, groups):
    if (len(types) == 0) or (request.user.is_authenticated and request.user.is_superuser):
        menu.append(page)
    else:
        is_group_in = False
        for g in groups:
            if g in user_groups:
                is_group_in = True
                break

        if 'login' in types and request.user.is_authenticated:
            menu.append(page)
        elif 'password' in types and request.user.is_authenticated and request.user.is_superuser:
            menu.append(page)
        elif 'groups' in types and is_group_in == True:
            menu.append(page)
    
    return menu


def make_menu(request, user_groups, indexes=None):
    if not indexes:
        home = Page.objects.get(title=settings.WAGTAIL_SITE_NAME)
        indexes = home.get_children().live().in_menu()

    menu = []
    for index in indexes:
        types, groups = get_page_restrictions(index)
        index.types = types
        index.groups = groups

        children = []
        pages = index.get_children().live().in_menu()
        if len(pages) > 0:
            for page in index.get_children().live().in_menu():
                ts, gs = get_page_restrictions(page)
                page.types = ts
                page.groups = gs

                childs = []
                posts = page.get_children().live().in_menu()
                if len(posts) > 0:
                    for post in posts:
                        t, g = get_page_restrictions(post)
                        post.types = t
                        post.groups = g
                        childs = add_menu(request, user_groups, childs, post, t, g)
                
                page.children = childs
                children = add_menu(request, user_groups, children, page, ts, gs)

        index.children = children

        menu = add_menu(request, user_groups, menu, index, types, groups)

    return menu