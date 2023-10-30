from django.conf import settings
from django.db import models
from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin

from core.functions import *


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items', on_delete=models.CASCADE)

class BlogPost(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]
    
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    def get_context(self, request):
        context = super(BlogPost, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['navbar_menu'] = make_menu(request, get_user_groups(request))
        context['sidebar_menu'] = make_menu(request, get_user_groups(request), self.get_parent().get_parent().get_children().live().in_menu())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f"/search/?query={tag.slug}&method=tag&page=1"
        return tags

class BlogPage(Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body'),
        FieldPanel('tags')
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = ['blog.BlogPost']

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['navbar_menu'] = make_menu(request, get_user_groups(request))
        context['sidebar_menu'] = make_menu(request, get_user_groups(request), self.get_parent().get_children().live().in_menu())
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = f"/search/?query={tag.slug}&method=tag&page=1"
        return tags


class BlogIndex(RoutablePageMixin, Page):
    publish_date = models.DateField('Publish date', blank=True, null=True)
    body = StreamField([
        ('visual', blocks.RichTextBlock(features=settings.RICH_TEXT_FEATURES)),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        FieldPanel('body')
    ]

    subpage_types = ['blog.BlogPage']

    def get_context(self, request):
        context = super(BlogIndex, self).get_context(request)
        context['model_name'] = self._meta.model_name
        context['navbar_menu'] = make_menu(request, get_user_groups(request))
        context['sidebar_menu'] = make_menu(request, get_user_groups(request), self.get_children().live().in_menu())
        return context


"""
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


def get_user_groups(request):
    return [ group.name for group in request.user.groups.all() ]
"""