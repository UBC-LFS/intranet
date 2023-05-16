from django.db import models
from django.apps import apps
from wagtail.models import Page

from django.conf import settings
from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.shortcuts import redirect, render


def get_app_name(app_label):
    app_name = ''
    if app_label == 'new_to_lfs':
        app_name = 'New to LFS'
    elif app_label == 'faculty_resources' or app_label == 'human_resources':
        words = app_label.split('_')
        labels = [ word.capitalize() for word in words ]
        app_name = ' '.join(labels)
    else:
        app_name = app_label.capitalize()
    return app_name


class PageModel(Page):
    class Meta:
        abstract = True
    
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
        FieldPanel('body'),
        FieldPanel('tags')
    ]

    subpage_types = []

    def get_context(self, request):
        context = super(PageModel, self).get_context(request)
        context['app_name'] = get_app_name(self._meta.app_label)
        context['model_name'] = self._meta.model_name
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags


class IndexModel(RoutablePageMixin, Page):
    class Meta:
        abstract = True

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
        FieldPanel('body'),
    ]

    def get_posts(self, tag=None):
        page_model = apps.get_model(app_label=self._meta.app_label, model_name=self._meta.model.subpage_types[0]) 
        posts = page_model.objects.child_of(self).live().order_by('-publish_date', 'title')
        
        if tag:
            posts = posts.filter(tags__name=tag)
        return posts

    def get_restriction_info(self, request, all_posts):
        user_groups = [ group.name for group in request.user.groups.all() ]

        posts = []
        for post in all_posts:
            is_public = True
            restriction_types = []
            restriction_groups = []
            
            if len(post.get_view_restrictions()) > 0:
                is_public = False
                for res in post.get_view_restrictions():
                    restriction_types.append(res.restriction_type)
                    for group in res.groups.all():
                        restriction_groups.append(group.name)
            else:
                restriction_types.append('public')
            
            post.restriction_types = restriction_types
            post.restriction_groups = restriction_groups

            groups = ', '.join(restriction_groups)
            
            if (is_public) or (request.user.is_authenticated and request.user.is_superuser):
                posts.append(post)
            else:
                if 'login' in restriction_types and request.user.is_authenticated:
                    posts.append(post)
                elif 'password' in restriction_types and request.user.is_authenticated and request.user.is_superuser:
                    posts.append(post)
                elif 'groups' in restriction_types and groups in user_groups:
                    posts.append(post)
        
        return posts

    def get_context(self, request):
        context = super(IndexModel, self).get_context(request)
        
        all_posts = self.get_posts()

        context['model_name'] = self._meta.model_name
        context['posts'] = self.get_restriction_info(request, all_posts)
        return context

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags

    @route(r"^tags/$", name="tag_archive")
    @route(r"^tags/([\w-]+)/$", name="tag_archive")
    def tag_archive(self, request, tag=None):
        app_label = self._meta.app_label
        template = '{0}/{0}_index.html'.format(app_label)
        all_posts = self.get_posts(tag=tag)
        context = { 
            'app_name': get_app_name(app_label), 
            'url': '/{0}/'.format(app_label.replace('_', '-')), 
            'tag': tag, 
            'posts': self.get_restriction_info(request, all_posts)
        }
        return render(request, template, context)